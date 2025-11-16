# Live USB - Portable Security Testing

Sec-Llama su USB bootable con persistenza completa per security testing portabile.

## 🚀 Quick Start

```bash
# Crea USB bootable (richiede sudo)
sudo ./create-usb.sh /dev/sdX

# Boot da USB
# All'avvio seleziona "Live USB with Persistence"

# Sec-Llama è già configurato e pronto!
```

## 💿 Cosa Include

### Base System
- **Kali Linux** o **Parrot Security OS** (scelta durante creazione)
- **Persistence** - Tutti i dati salvati permanentemente
- **Sec-Llama** - Pre-installato e configurato
- **Ollama** - LLM locale con modelli pre-scaricati
- **Security Tools** - Suite completa strumenti

### Pre-configured Features
- ✅ Sec-Llama completamente configurato
- ✅ Ollama con modello llama3.1:8b
- ✅ Database SQLite con persistenza
- ✅ Reports salvati su USB
- ✅ Network tools pre-configurati
- ✅ Web UI accessibile

## 📦 Requisiti

### Hardware
- **USB Drive**: 32GB+ (64GB raccomandato)
- **RAM**: 8GB+ (16GB raccomandato per LLM)
- **CPU**: x86_64 (64-bit)
- **GPU**: NVIDIA (opzionale, per LLM più veloci)

### Software (per creazione)
- **Linux** - Sistema Linux per creare USB
- **dd/rufus** - Tool per scrivere immagine
- **sudo** - Privilegi root

## 🔧 Creazione USB

### Metodo Automatico (Raccomandato)

```bash
# Download script
cd implementations/live-usb

# Rendi eseguibile
chmod +x create-usb.sh

# Crea USB (ATTENZIONE: cancella tutto su USB!)
sudo ./create-usb.sh /dev/sdX

# Segui le istruzioni
```

Lo script:
1. Scarica ISO Kali/Parrot
2. Verifica checksum
3. Crea partizione persistenza
4. Scrive immagine ISO
5. Configura boot persistence
6. Installa Sec-Llama
7. Pre-scarica modelli Ollama

### Metodo Manuale

#### 1. Scarica ISO

**Kali Linux:**
```bash
wget https://cdimage.kali.org/kali-2024.1/kali-linux-2024.1-installer-amd64.iso
```

**Parrot Security:**
```bash
wget https://download.parrot.sh/parrot/iso/5.3/Parrot-security-5.3_amd64.iso
```

#### 2. Crea USB con Persistenza

```bash
# Identifica USB
lsblk

# Scrivi ISO (ATTENZIONE: sostituisci sdX!)
sudo dd if=kali-linux-2024.1-installer-amd64.iso of=/dev/sdX bs=4M status=progress
sync

# Crea partizione persistence
sudo fdisk /dev/sdX
# n (new partition)
# p (primary)
# Enter (default start)
# Enter (default end)
# w (write)

# Formatta persistence
sudo mkfs.ext4 -L persistence /dev/sdX3

# Monta e configura
sudo mkdir -p /mnt/usb
sudo mount /dev/sdX3 /mnt/usb
echo "/ union" | sudo tee /mnt/usb/persistence.conf
sudo umount /mnt/usb
```

#### 3. Boot e Install Sec-Llama

```bash
# Boot da USB
# Seleziona "Live USB Persistence"

# Installa Sec-Llama
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama/implementations/standalone
./setup.sh

# Installa Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```

## 🎨 Utilizzo

### Boot

1. **Inserisci USB** nel computer target
2. **Accedi al boot menu** (F12/F2/ESC/DEL)
3. **Seleziona USB drive**
4. **Scegli**: "Live USB with Persistence"
5. **Login**: Credenziali standard Kali/Parrot

### Sec-Llama sul Live USB

```bash
# CLI mode
cd /home/kali/Sec-llama/implementations/standalone
./sec-llama.sh scan network 192.168.1.0/24

# Web UI mode
cd /home/kali/Sec-llama/implementations/web-ui-full
./start.sh
# Apri browser: http://localhost:8080

# MCP mode (per Claude Desktop su altro PC)
cd /home/kali/Sec-llama/implementations/mcp-http
./start.sh
# Access da: http://USB_IP:8765
```

### Storage Esterno per Modelli

Per modelli LLM grandi, usa storage esterno:

```bash
# Monta storage esterno
sudo mkdir -p /mnt/external
sudo mount /dev/sdb1 /mnt/external

# Configura Ollama
export OLLAMA_MODELS=/mnt/external/ollama_models
mkdir -p $OLLAMA_MODELS

# Pull modelli su storage esterno
ollama pull llama3.1:70b
```

### Salvataggio Reports

Reports vengono salvati su persistenza USB:

```bash
# Verifica reports salvati
ls -la /home/kali/Sec-llama/reports/

# Copia su storage esterno
cp -r /home/kali/Sec-llama/reports/* /mnt/external/reports/
```

## 🔒 Sicurezza

### Encryption

Per dati sensibili, usa encryption:

```bash
# Durante creazione USB, cripta partizione persistence
sudo cryptsetup luksFormat /dev/sdX3
sudo cryptsetup luksOpen /dev/sdX3 persistence
sudo mkfs.ext4 -L persistence /dev/mapper/persistence

# All'avvio, inserisci password per sbloccare
```

### Secure Erase

Quando finito, cancella dati:

```bash
# Wipe USB completamente
sudo dd if=/dev/zero of=/dev/sdX bs=4M status=progress

# O usa shred
sudo shred -vfz -n 3 /dev/sdX
```

## 📊 Features Speciali

### Network Configuration

Live USB rileva automaticamente:
- Ethernet adapters
- WiFi adapters (con drivers)
- USB network adapters

### Wireless Tools Pre-configured

```bash
# WiFi scanning
airmon-ng start wlan0
airodump-ng wlan0mon

# Con Sec-Llama
./sec-llama.sh wireless scan --interface wlan0
```

### GPU Acceleration

Se hai NVIDIA GPU:

```bash
# Install drivers (se non inclusi)
sudo apt update
sudo apt install nvidia-driver nvidia-cuda-toolkit

# Verifica
nvidia-smi

# Ollama userà GPU automaticamente
```

## 🔄 Aggiornamenti

### Update Sec-Llama

```bash
cd /home/kali/Sec-llama
git pull origin main

# Update implementazioni
cd implementations/standalone
./setup.sh
```

### Update Sistema

```bash
sudo apt update
sudo apt upgrade

# Update Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### Update Modelli

```bash
# Pull nuovo modello
ollama pull llama3.1:latest

# Remove vecchio
ollama rm llama3.1:8b
```

## 🆘 Troubleshooting

### USB non boota

1. **Verifica boot order** nel BIOS/UEFI
2. **Disabilita Secure Boot** (se necessario)
3. **Usa UEFI mode** (raccomandato)
4. **Ricrea USB** con tool diverso (Rufus su Windows, Etcher)

### Persistence non funziona

```bash
# Verifica partizione
lsblk -f

# Controlla persistence.conf
sudo mount /dev/sdX3 /mnt/usb
cat /mnt/usb/persistence.conf
# Deve contenere: / union
```

### Ollama out of memory

```bash
# Usa modello più piccolo
ollama pull phi:latest  # 2.7B params
ollama pull llama3.1:8b  # 8B params invece di 70B

# O aumenta swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### WiFi adapter non funziona

```bash
# Verifica supporto
lsusb
lspci | grep -i network

# Install firmware
sudo apt update
sudo apt install firmware-linux firmware-linux-nonfree

# Reboot
sudo reboot
```

### Spazio insufficiente

```bash
# Check spazio
df -h

# Pulisci cache
sudo apt clean
sudo apt autoclean

# Remove vecchi kernels
sudo apt autoremove

# Usa storage esterno per reports/modelli
```

## 🎯 Use Cases

### 1. Penetration Testing On-Site

```bash
# Boot USB on client network
# Run full assessment
./sec-llama.sh scan network --full
./sec-llama.sh report generate --format pdf

# Export report to external drive
cp reports/* /mnt/external/
```

### 2. Incident Response

```bash
# Boot on compromised system
# Collect evidence
./sec-llama.sh incident create --title "Breach Response"
./sec-llama.sh logs analyze --file /var/log/auth.log

# Save findings
cp -r database/ /mnt/external/evidence/
```

### 3. Training & Demos

```bash
# Boot USB for training
# All tools available immediately
# No installation needed
# Isolated from host system
```

### 4. Privacy-Focused Analysis

```bash
# Analyze sensitive data offline
# No network connection required
# All processing local
# Wipe when done
```

## 📚 Backup & Restore

### Backup USB

```bash
# Clone intera USB
sudo dd if=/dev/sdX of=usb_backup.img bs=4M status=progress

# Compress
gzip usb_backup.img

# Restore
gunzip usb_backup.img.gz
sudo dd if=usb_backup.img of=/dev/sdX bs=4M status=progress
```

### Backup Solo Persistence

```bash
# Backup dati utente
sudo mount /dev/sdX3 /mnt/usb
sudo tar czf persistence_backup.tar.gz -C /mnt/usb .
sudo umount /mnt/usb

# Restore
sudo mount /dev/sdX3 /mnt/usb
sudo tar xzf persistence_backup.tar.gz -C /mnt/usb
sudo umount /mnt/usb
```

## 🔗 Resources

- **[Kali Linux](https://www.kali.org/)** - Official Kali Linux
- **[Parrot Security](https://www.parrotsec.org/)** - Official Parrot Security
- **[Persistence Guide](https://www.kali.org/docs/usb/kali-linux-live-usb-persistence/)** - Kali persistence docs
- **[Sec-Llama Main](../../README.md)** - Main documentation

## 📝 Customization

### Custom Tools

Aggiungi i tuoi tool preferiti:

```bash
# Install tool
sudo apt install your-tool

# Add to persistence
echo "your-tool" >> /home/kali/.tools_list
```

### Auto-start Services

```bash
# Create systemd service
sudo nano /etc/systemd/system/sec-llama-web.service

[Unit]
Description=Sec-Llama Web UI
After=network.target

[Service]
Type=simple
User=kali
WorkingDirectory=/home/kali/Sec-llama/implementations/web-ui-full
ExecStart=/home/kali/Sec-llama/implementations/web-ui-full/start.sh
Restart=always

[Install]
WantedBy=multi-user.target

# Enable
sudo systemctl enable sec-llama-web
```

---

**ATTENZIONE:** Usa solo su hardware di tua proprietà o con autorizzazione esplicita. Il Live USB è uno strumento potente - usalo responsabilmente.
