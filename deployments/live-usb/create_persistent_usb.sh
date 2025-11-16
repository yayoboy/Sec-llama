#!/bin/bash
# Script per creare USB Kali Linux Live con Persistenza
# Uso: sudo ./create_persistent_usb.sh /dev/sdX kali-linux-2024.iso 32GB

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funzioni helper
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica argomenti
if [ "$#" -lt 2 ]; then
    echo "Uso: $0 <device> <iso_file> [persistence_size]"
    echo "Esempio: $0 /dev/sdb kali-linux-2024.iso 32GB"
    exit 1
fi

DEVICE=$1
ISO_FILE=$2
PERSISTENCE_SIZE=${3:-16GB}

# Verifica se eseguito come root
if [ "$EUID" -ne 0 ]; then
    print_error "Questo script deve essere eseguito come root"
    exit 1
fi

# Verifica se il device esiste
if [ ! -b "$DEVICE" ]; then
    print_error "Device $DEVICE non trovato"
    exit 1
fi

# Verifica se l'ISO esiste
if [ ! -f "$ISO_FILE" ]; then
    print_error "File ISO $ISO_FILE non trovato"
    exit 1
fi

# Warning
print_warning "ATTENZIONE: Tutti i dati su $DEVICE verranno cancellati!"
print_warning "Device: $DEVICE"
print_warning "ISO: $ISO_FILE"
print_warning "Dimensione persistenza: $PERSISTENCE_SIZE"
read -p "Continuare? (yes/no): " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    print_info "Operazione annullata"
    exit 0
fi

# Step 1: Scrivi ISO su USB
print_info "Step 1/5: Scrittura ISO su USB..."
dd if="$ISO_FILE" of="$DEVICE" bs=4M status=progress oflag=sync
sync

# Step 2: Verifica partizioni
print_info "Step 2/5: Verifica partizioni..."
sleep 2
partprobe "$DEVICE"
fdisk -l "$DEVICE"

# Step 3: Crea partizione di persistenza
print_info "Step 3/5: Creazione partizione di persistenza..."

# Trova l'ultimo settore della partizione ISO
END_SECTOR=$(parted "$DEVICE" unit s print | grep "^ 2" | awk '{print $3}' | sed 's/s//')
if [ -z "$END_SECTOR" ]; then
    # Se c'è solo una partizione, usa quella
    END_SECTOR=$(parted "$DEVICE" unit s print | grep "^ 1" | awk '{print $3}' | sed 's/s//')
fi

print_info "Creazione nuova partizione dopo settore $END_SECTOR"

# Crea partizione di persistenza (userà tutto lo spazio rimanente)
parted "$DEVICE" mkpart primary ext4 ${END_SECTOR}s 100%
partprobe "$DEVICE"
sleep 2

# Determina il nome della partizione di persistenza
if [[ "$DEVICE" == *"nvme"* ]] || [[ "$DEVICE" == *"mmcblk"* ]]; then
    PERSISTENCE_PART="${DEVICE}p3"
else
    PERSISTENCE_PART="${DEVICE}3"
fi

# Step 4: Formatta e label la partizione di persistenza
print_info "Step 4/5: Formattazione partizione di persistenza..."
mkfs.ext4 -F -L persistence "$PERSISTENCE_PART"

# Step 5: Configura la persistenza
print_info "Step 5/5: Configurazione persistenza..."
MOUNT_POINT=$(mktemp -d)
mount "$PERSISTENCE_PART" "$MOUNT_POINT"

# Crea file persistence.conf
echo "/ union" > "$MOUNT_POINT/persistence.conf"

# Crea directory per Sec-Llama
mkdir -p "$MOUNT_POINT/root/sec-llama"
mkdir -p "$MOUNT_POINT/opt/ollama-models"

umount "$MOUNT_POINT"
rmdir "$MOUNT_POINT"

sync

print_info "✓ USB Live con Persistenza creato con successo!"
print_info ""
print_info "Configurazione completata:"
print_info "  - Device: $DEVICE"
print_info "  - Partizione ISO: ${DEVICE}1 e ${DEVICE}2"
print_info "  - Partizione persistenza: $PERSISTENCE_PART"
print_info ""
print_info "Al boot di Kali Live, seleziona 'Live USB Persistence' dal menu GRUB"
print_info ""
print_info "Dopo il boot, esegui: /root/sec-llama/scripts/setup_persistent_env.sh"
