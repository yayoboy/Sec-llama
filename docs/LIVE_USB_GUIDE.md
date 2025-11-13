# 💾 Guida Completa: Sec-Llama su Live USB con Persistenza

Questa guida spiega **tutti i metodi** per salvare dati quando usi Sec-Llama su una distribuzione Linux Live da pendrive.

---

## 📋 Indice

1. [Opzioni di Persistenza](#opzioni-di-persistenza)
2. [Metodo 1: USB con Persistenza Nativa](#metodo-1-usb-con-persistenza-nativa)
3. [Metodo 2: Partizione Dati Separata](#metodo-2-partizione-dati-separata)
4. [Metodo 3: Storage Esterno](#metodo-3-storage-esterno)
5. [Metodo 4: LLM Remoto](#metodo-4-llm-remoto)
6. [Confronto Metodi](#confronto-metodi)
7. [Backup e Ripristino](#backup-e-ripristino)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Opzioni di Persistenza

### **Sì, puoi salvare TUTTI i dati!** Ecco come:

| Metodo | Persistenza | Complessità | Spazio Richiesto | Prestazioni |
|--------|-------------|-------------|------------------|-------------|
| USB Persistence | ✅ Completa | 🟢 Bassa | 32GB+ | ⭐⭐⭐ |
| Partizione Separata | ✅ Solo dati | 🟡 Media | 16GB+ | ⭐⭐⭐⭐ |
| Storage Esterno | ✅ Modelli/Reports | 🟢 Bassa | 64GB+ | ⭐⭐⭐⭐⭐ |
| LLM Remoto | ⚠️ Solo config | 🟢 Bassa | 8GB | ⭐⭐⭐⭐⭐ |

---

## 🔧 Metodo 1: USB con Persistenza Nativa

### ✅ Vantaggi
- Sistema completo persistente (pacchetti, configurazioni, file)
- Modelli LLM salvati permanentemente
- Risultati e database persistenti
- Esperienza identica a installazione normale

### ⚠️ Svantaggi
- Richiede USB capiente (64GB+ raccomandato)
- Performance I/O dipendente da velocità USB
- Usura USB più rapida

### 📝 Setup

#### **Opzione A: Durante Creazione USB (Raccomandato)**

Usa lo script automatico fornito:

```bash
# Su Linux (per creare USB)
sudo ./scripts/create_persistent_usb.sh /dev/sdX kali-linux-2024.iso 32GB

# Dove:
#   /dev/sdX = tuo dispositivo USB (ATTENZIONE: verifica con lsblk!)
#   kali-linux-2024.iso = file ISO Kali
#   32GB = dimensione partizione persistenza
```

**Cosa fa lo script:**
1. Scrive ISO su USB
2. Crea partizione persistenza con spazio rimanente
3. Formatta e configura persistenza
4. Crea directory per Sec-Llama

#### **Opzione B: Post-Installazione Manuale**

Se hai già USB live senza persistenza:

```bash
# 1. Identifica USB
lsblk

# 2. Crea partizione (esempio: /dev/sdb)
sudo parted /dev/sdb mkpart primary ext4 4GB 100%

# 3. Formatta con label "persistence"
sudo mkfs.ext4 -F -L persistence /dev/sdb3

# 4. Monta e configura
sudo mkdir /mnt/usb-persistence
sudo mount /dev/sdb3 /mnt/usb-persistence
echo "/ union" | sudo tee /mnt/usb-persistence/persistence.conf

# 5. Crea directory Sec-Llama
sudo mkdir -p /mnt/usb-persistence/root/sec-llama
sudo mkdir -p /mnt/usb-persistence/opt/ollama-models

sudo umount /mnt/usb-persistence
```

### 🚀 Primo Boot con Persistenza

1. **Boot da USB**
2. **Seleziona "Live USB Persistence"** dal menu GRUB
3. **Esegui setup automatico:**

```bash
# Scarica Sec-Llama
cd /root
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama

# Esegui setup automatico
sudo bash scripts/setup_persistent_env.sh
```

Lo script installerà:
- ✅ Ollama + modello Llama 3.1 8B quantizzato
- ✅ Tool di sicurezza (nmap, masscan, wireshark, aircrack-ng)
- ✅ Sec-Llama con tutte le dipendenze
- ✅ Configurazione ottimizzata per live USB

### 📊 Verifica Persistenza

```bash
# Crea file di test
echo "test" > /root/test-persistence.txt

# Riavvia
reboot

# Dopo riavvio, verifica
cat /root/test-persistence.txt  # Dovrebbe mostrare "test"
```

---

## 🗂️ Metodo 2: Partizione Dati Separata

Usa persistenza OS + partizione separata per dati pesanti.

### 📝 Setup

```bash
# 1. Crea partizione dati (esempio: 40GB)
sudo parted /dev/sdb mkpart primary ext4 36GB 76GB
sudo mkfs.ext4 -L sec-llama-data /dev/sdb4

# 2. Monta partizione dati
sudo mkdir -p /mnt/sec-data
sudo mount /dev/sdb4 /mnt/sec-data

# 3. Crea directory
sudo mkdir -p /mnt/sec-data/ollama-models
sudo mkdir -p /mnt/sec-data/reports
sudo mkdir -p /mnt/sec-data/datasets

# 4. Link simbolici
ln -s /mnt/sec-data/ollama-models /opt/ollama-models
ln -s /mnt/sec-data/reports /root/sec-llama/reports
ln -s /mnt/sec-data/datasets /root/sec-llama/datasets

# 5. Configura Ollama
export OLLAMA_MODELS=/mnt/sec-data/ollama-models
echo 'export OLLAMA_MODELS=/mnt/sec-data/ollama-models' >> ~/.bashrc
```

### 🔄 Auto-Mount al Boot

Aggiungi a `/etc/fstab` (nella persistenza):

```bash
# Ottieni UUID
sudo blkid /dev/sdb4

# Aggiungi a /etc/fstab
UUID=xxx-xxx-xxx  /mnt/sec-data  ext4  defaults  0  2
```

---

## 💿 Metodo 3: Storage Esterno

Usa disco/SSD esterno per modelli LLM (migliore performance).

### ✅ Vantaggi
- SSD esterno = performance superiori
- Modelli accessibili da più sistemi
- Non consuma spazio USB live

### 📝 Setup Automatico

Usa lo script fornito:

```bash
# Esegui script interattivo
sudo bash scripts/external_models_storage.sh

# O setup diretto
sudo bash scripts/external_models_storage.sh sdc1  # device esterno
```

**Lo script:**
1. Rileva storage esterno
2. Monta dispositivo
3. Configura Ollama per usare storage esterno
4. Opzionalmente migra modelli esistenti
5. Configura auto-mount

### 📝 Setup Manuale

```bash
# 1. Collega disco esterno e identifica
lsblk

# 2. Monta (esempio: /dev/sdc1)
sudo mkdir -p /mnt/ollama-external
sudo mount /dev/sdc1 /mnt/ollama-external

# 3. Crea directory modelli
sudo mkdir -p /mnt/ollama-external/ollama-models

# 4. Configura Ollama
export OLLAMA_MODELS=/mnt/ollama-external/ollama-models
echo 'export OLLAMA_MODELS=/mnt/ollama-external/ollama-models' >> ~/.bashrc

# 5. Riavvia Ollama
sudo systemctl restart ollama
# O se non systemd:
pkill ollama && nohup ollama serve &

# 6. Testa
ollama list  # Verifica percorso
```

### 🔐 Storage Esterno Cifrato (Opzionale)

Per proteggere modelli e dati sensibili:

```bash
# 1. Setup LUKS
sudo cryptsetup luksFormat /dev/sdc1
sudo cryptsetup open /dev/sdc1 sec-llama-vault

# 2. Formatta
sudo mkfs.ext4 /dev/mapper/sec-llama-vault

# 3. Monta
sudo mount /dev/mapper/sec-llama-vault /mnt/ollama-external

# Al boot, sblocca con:
sudo cryptsetup open /dev/sdc1 sec-llama-vault
sudo mount /dev/mapper/sec-llama-vault /mnt/ollama-external
```

---

## 🌐 Metodo 4: LLM Remoto (Ollama Server)

Usa Ollama su server remoto, live USB solo per tool.

### ✅ Vantaggi
- Live USB leggerissima (solo ~8GB)
- Modelli grandi (70B, 405B) accessibili
- Performance migliori (GPU server)
- Zero persistenza necessaria su USB

### ⚠️ Requisiti
- Server Linux/macOS/Windows con Ollama
- Connettività di rete tra live USB e server

### 📝 Setup Server

```bash
# Su server (Linux/macOS)
# 1. Installa Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Configura per accesso remoto
export OLLAMA_HOST=0.0.0.0:11434

# 3. Avvia servizio
ollama serve

# 4. Pull modelli
ollama pull llama3.1:70b
ollama pull mistral
```

### 📝 Setup Client (Live USB)

```bash
# Su Kali Live (o altra distro)
# 1. Configura endpoint remoto
export OLLAMA_HOST=http://192.168.1.100:11434

# 2. Testa connessione
curl http://192.168.1.100:11434/api/tags

# 3. Installa solo Sec-Llama (senza Ollama locale)
git clone https://github.com/yourusername/Sec-llama.git
cd Sec-llama
pip3 install -r requirements.txt

# 4. Configura
cat > config/config.yaml << EOF
llm:
  provider: "ollama"
  model: "llama3.1:70b"
  base_url: "http://192.168.1.100:11434"  # Server IP
  timeout: 120
EOF

# 5. Usa normalmente
sec-llama network discover 192.168.1.0/24
```

### 🔐 Setup con Tunnel SSH (Più Sicuro)

```bash
# Su live USB, crea tunnel SSH verso server
ssh -L 11434:localhost:11434 user@192.168.1.100 -N -f

# Configura Ollama per usare tunnel locale
export OLLAMA_HOST=http://localhost:11434

# Ora usa Sec-Llama normalmente
sec-llama --help
```

---

## ⚖️ Confronto Metodi

### Per Penetration Testing Occasionale
**🏆 Raccomandato: Storage Esterno (SSD USB-C)**
- USB Live 16GB (sistema + tool)
- SSD esterno 256GB (modelli + dati)
- Performance ottime, portabile

### Per Uso Regolare/Professionale
**🏆 Raccomandato: USB Persistenza + LLM Remoto**
- USB 32GB con persistenza (tool + config)
- Server casa con modelli grandi + GPU
- Flessibilità massima

### Per Laboratorio/Training
**🏆 Raccomandato: USB Persistenza Completa**
- USB 128GB+ con persistenza
- Tutto self-contained
- Funziona offline

---

## 💾 Backup e Ripristino

### Backup Automatico

Usa lo script fornito:

```bash
# Backup completo su storage esterno
sudo bash scripts/backup_data.sh /media/backup-usb

# Cosa viene salvato:
# - Configurazione (config.yaml)
# - Reports generati
# - Database scansioni
# - Logs (opzionale)
# - Training datasets
# - Lista modelli custom
```

### Backup Manuale Rapido

```bash
# Backup essenziale
tar -czf sec-llama-backup.tar.gz \
    /root/sec-llama/config/config.yaml \
    /root/sec-llama/reports/ \
    /root/sec-llama/database/

# Copia su storage esterno
cp sec-llama-backup.tar.gz /media/backup-usb/
```

### Ripristino

```bash
# 1. Estrai backup
tar -xzf sec-llama-backup.tar.gz -C /

# 2. Verifica permessi
chown -R root:root /root/sec-llama

# 3. Riavvia servizi
systemctl restart ollama
```

### Sync Cloud (Opzionale)

```bash
# Setup rclone per Google Drive/Dropbox
apt install rclone
rclone config

# Backup automatico reports su cloud
rclone sync /root/sec-llama/reports gdrive:sec-llama-reports

# Aggiungi a cron per backup periodico
echo "0 2 * * * rclone sync /root/sec-llama/reports gdrive:sec-llama-reports" | crontab -
```

---

## 🔧 Troubleshooting

### Persistenza Non Funziona

```bash
# Verifica se partizione persistenza esiste
lsblk -f | grep persistence

# Verifica file persistence.conf
cat /run/live/persistence/sdb3/persistence.conf
# Dovrebbe contenere: / union

# Verifica mount
mount | grep persistence
```

### Spazio Insufficiente

```bash
# Verifica spazio usato
df -h

# Pulisci cache
apt clean
rm -rf /var/cache/apt/*

# Pulisci vecchi logs
journalctl --vacuum-size=100M

# Rimuovi modelli non usati
ollama rm model-name
```

### Ollama Non Trova Modelli

```bash
# Verifica variabile ambiente
echo $OLLAMA_MODELS

# Verifica processo Ollama
ps aux | grep ollama

# Riavvia Ollama
pkill ollama
export OLLAMA_MODELS=/percorso/corretto
ollama serve
```

### Performance Lente

```bash
# Verifica velocità USB
hdparm -t /dev/sdb

# Disabilita journal ext4 (più veloce ma meno sicuro)
tune2fs -O ^has_journal /dev/sdb3

# Usa profilo "live_quick" per scan
sec-llama network discover --profile live_quick 192.168.1.0/24
```

### Modello Non Si Carica (Out of Memory)

```bash
# Usa modello quantizzato più piccolo
ollama pull llama3.1:8b-instruct-q4_K_M  # ~4.5GB invece di 8GB

# O usa mistral (più leggero)
ollama pull mistral:7b-instruct-q4_0  # ~3.8GB

# Aggiorna config
sed -i 's/llama3.1:8b/llama3.1:8b-instruct-q4_K_M/' /root/sec-llama/config/config.yaml
```

---

## 📚 Risorse Aggiuntive

### Script Forniti

- `create_persistent_usb.sh` - Crea USB con persistenza
- `setup_persistent_env.sh` - Setup completo Sec-Llama
- `backup_data.sh` - Backup automatico
- `external_models_storage.sh` - Gestione storage esterno

### Comandi Rapidi

```bash
# Verifica configurazione
sec-llama config show

# Test rapido
sec-llama network discover 192.168.1.1/24 --quick

# Backup rapido
sec-llama report export --format json

# Lista modelli
ollama list

# Spazio disponibile
df -h /opt/ollama-models
```

### Link Utili

- [Kali Linux Persistence](https://www.kali.org/docs/usb/kali-linux-live-usb-persistence/)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [Sec-Llama README](../README.md)

---

## ✅ Conclusione

**Risposta breve:** SÌ, puoi salvare TUTTI i dati su live USB!

**Metodo raccomandato per la maggior parte degli utenti:**
1. USB 64GB+ con persistenza nativa
2. Storage esterno SSD per modelli LLM grandi
3. Backup periodici su cloud/disco esterno

Questo setup offre:
- ✅ Portabilità completa
- ✅ Performance ottime
- ✅ Sicurezza (tutto locale)
- ✅ Flessibilità (funziona offline)

---

**Domande?** Consulta la [documentazione completa](../README.md) o apri una issue su GitHub.
