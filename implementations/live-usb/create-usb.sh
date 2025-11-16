#!/bin/bash
# Live USB - USB Creation Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   echo "Usage: sudo $0 /dev/sdX"
   exit 1
fi

# Check argument
if [ $# -eq 0 ]; then
    echo -e "${RED}No USB device specified${NC}"
    echo "Usage: sudo $0 /dev/sdX"
    echo ""
    echo "Available devices:"
    lsblk -d -o NAME,SIZE,TYPE | grep disk
    exit 1
fi

USB_DEVICE=$1

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         Sec-Llama Live USB Creator                       ║
║         Bootable Security Testing Platform               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verify device
if [ ! -b "$USB_DEVICE" ]; then
    echo -e "${RED}Device $USB_DEVICE not found${NC}"
    exit 1
fi

# Check if device is USB
if ! udevadm info --query=all --name=$USB_DEVICE | grep -q "ID_BUS=usb"; then
    echo -e "${YELLOW}WARNING: $USB_DEVICE may not be a USB device${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get device size
DEVICE_SIZE=$(lsblk -b -d -n -o SIZE $USB_DEVICE)
DEVICE_SIZE_GB=$((DEVICE_SIZE / 1024 / 1024 / 1024))

echo -e "${BLUE}Device Information:${NC}"
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT $USB_DEVICE
echo ""

if [ $DEVICE_SIZE_GB -lt 16 ]; then
    echo -e "${RED}USB device too small (${DEVICE_SIZE_GB}GB). Minimum 32GB recommended.${NC}"
    exit 1
fi

echo -e "${YELLOW}WARNING: ALL DATA ON $USB_DEVICE WILL BE DESTROYED!${NC}"
echo ""
read -p "Are you sure you want to continue? (type 'yes'): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Choose distribution
echo ""
echo -e "${BLUE}Choose base distribution:${NC}"
echo "1) Kali Linux (Recommended)"
echo "2) Parrot Security OS"
read -p "Choice (1 or 2): " DISTRO_CHOICE

case $DISTRO_CHOICE in
    1)
        DISTRO="kali"
        ISO_URL="https://cdimage.kali.org/kali-2024.1/kali-linux-2024.1-installer-amd64.iso"
        ISO_NAME="kali-linux-2024.1-installer-amd64.iso"
        ;;
    2)
        DISTRO="parrot"
        ISO_URL="https://download.parrot.sh/parrot/iso/5.3/Parrot-security-5.3_amd64.iso"
        ISO_NAME="Parrot-security-5.3_amd64.iso"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Download ISO if not present
echo ""
echo -e "${BLUE}Step 1/6: Downloading ISO...${NC}"

if [ ! -f "$ISO_NAME" ]; then
    echo "Downloading $ISO_NAME..."
    wget -c "$ISO_URL" -O "$ISO_NAME"
else
    echo "ISO already downloaded: $ISO_NAME"
fi

# Verify ISO (optional but recommended)
echo ""
echo -e "${BLUE}Step 2/6: Verifying ISO...${NC}"
echo "Calculating checksum..."
sha256sum "$ISO_NAME"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Unmount device
echo ""
echo -e "${BLUE}Step 3/6: Preparing USB device...${NC}"

for part in ${USB_DEVICE}* ; do
    if [ "$part" != "$USB_DEVICE" ]; then
        umount $part 2>/dev/null || true
    fi
done

# Write ISO to USB
echo ""
echo -e "${BLUE}Step 4/6: Writing ISO to USB (this may take 10-20 minutes)...${NC}"

dd if="$ISO_NAME" of="$USB_DEVICE" bs=4M status=progress oflag=sync
sync

echo -e "${GREEN}✓ ISO written successfully${NC}"

# Create persistence partition
echo ""
echo -e "${BLUE}Step 5/6: Creating persistence partition...${NC}"

# Wait for device to settle
sleep 3
partprobe $USB_DEVICE
sleep 2

# Find last partition number
LAST_PART=$(lsblk -n -o NAME $USB_DEVICE | tail -1 | grep -o '[0-9]*$')
NEXT_PART=$((LAST_PART + 1))
PERSIST_PART="${USB_DEVICE}${NEXT_PART}"

# Create new partition for persistence
echo "Creating partition ${PERSIST_PART}..."
(
echo n  # New partition
echo    # Default partition number
echo    # Default first sector
echo    # Default last sector (use remaining space)
echo w  # Write changes
) | fdisk $USB_DEVICE 2>/dev/null || true

# Wait for partition to appear
sleep 3
partprobe $USB_DEVICE
sleep 2

# Format persistence partition
echo "Formatting persistence partition..."
mkfs.ext4 -F -L persistence $PERSIST_PART

# Configure persistence
echo "Configuring persistence..."
MOUNT_POINT=$(mktemp -d)
mount $PERSIST_PART $MOUNT_POINT
echo "/ union" > $MOUNT_POINT/persistence.conf
umount $MOUNT_POINT
rmdir $MOUNT_POINT

echo -e "${GREEN}✓ Persistence configured${NC}"

# Install Sec-Llama (prepare script)
echo ""
echo -e "${BLUE}Step 6/6: Preparing Sec-Llama installation...${NC}"

MOUNT_POINT=$(mktemp -d)
mount $PERSIST_PART $MOUNT_POINT

# Create firstboot script
cat > $MOUNT_POINT/setup-sec-llama.sh << 'FIRSTBOOT'
#!/bin/bash
# Sec-Llama First Boot Setup

echo "🚀 Setting up Sec-Llama..."

# Update system
apt update

# Install dependencies
apt install -y git python3 python3-pip python3-venv curl

# Clone Sec-Llama
cd /home/kali
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Setup standalone implementation
cd implementations/standalone
./setup.sh

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull default model
ollama serve &
sleep 10
ollama pull llama3.1:8b

# Create desktop shortcut
cat > /home/kali/Desktop/sec-llama.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Sec-Llama
Comment=Local LLM Security Suite
Exec=/home/kali/Sec-llama/implementations/standalone/sec-llama.sh
Icon=security-high
Terminal=true
Categories=Security;
DESKTOP

chmod +x /home/kali/Desktop/sec-llama.desktop
chown kali:kali /home/kali/Desktop/sec-llama.desktop

echo "✅ Sec-Llama setup complete!"
echo ""
echo "Usage:"
echo "  cd /home/kali/Sec-llama/implementations/standalone"
echo "  ./sec-llama.sh --help"
FIRSTBOOT

chmod +x $MOUNT_POINT/setup-sec-llama.sh

# Create README
cat > $MOUNT_POINT/README-SEC-LLAMA.txt << 'README'
Sec-Llama Live USB
==================

This USB contains a bootable security testing platform with Sec-Llama pre-configured.

Boot Instructions:
1. Insert USB into target computer
2. Access boot menu (F12/F2/ESC/DEL)
3. Select USB drive
4. Choose "Live USB with Persistence"

First Boot:
- Run: sudo /setup-sec-llama.sh
- This will install Sec-Llama and Ollama
- Takes ~15 minutes depending on internet speed

Usage:
- CLI: /home/kali/Sec-llama/implementations/standalone/sec-llama.sh
- Web UI: /home/kali/Sec-llama/implementations/web-ui-full/start.sh

All data is saved to the persistence partition.

For more info: https://github.com/yourusername/Sec-llama
README

umount $MOUNT_POINT
rmdir $MOUNT_POINT

echo -e "${GREEN}✓ Sec-Llama installation prepared${NC}"

# Summary
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║         Live USB Created Successfully!                   ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Device:${NC} $USB_DEVICE"
echo -e "${BLUE}Distribution:${NC} $DISTRO"
echo -e "${BLUE}Persistence:${NC} Enabled ($PERSIST_PART)"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Remove USB safely"
echo "2. Boot from USB on target computer"
echo "3. Select 'Live USB with Persistence'"
echo "4. Run: ${YELLOW}sudo /setup-sec-llama.sh${NC}"
echo ""
echo -e "${BLUE}Important:${NC}"
echo "- First boot setup takes ~15 minutes"
echo "- Requires internet connection for setup"
echo "- All data persists across reboots"
echo ""
echo -e "${YELLOW}Note: Read /README-SEC-LLAMA.txt on the persistence partition${NC}"
echo ""
