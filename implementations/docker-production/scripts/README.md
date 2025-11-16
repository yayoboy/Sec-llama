# 🛠️ Script per Live USB con Persistenza

Questa directory contiene script per configurare e gestire Sec-Llama su distribuzioni Linux Live con persistenza dati.

## 📋 Script Disponibili

### 1. `create_persistent_usb.sh` - Crea USB Bootable con Persistenza

Crea una USB bootable Kali Linux (o altra distro) con partizione di persistenza.

**Uso:**
```bash
sudo ./create_persistent_usb.sh <device> <iso_file> [persistence_size]
```

**Esempio:**
```bash
# Crea USB da 64GB con 32GB di persistenza
sudo ./create_persistent_usb.sh /dev/sdb kali-linux-2024.iso 32GB
```

**⚠️ ATTENZIONE:** Tutti i dati sul device verranno cancellati!

**Cosa fa:**
- Scrive ISO su USB
- Crea partizione di persistenza con spazio rimanente
- Configura persistenza automatica
- Crea directory per Sec-Llama e modelli Ollama

---

### 2. `setup_persistent_env.sh` - Setup Ambiente Persistente

Installa e configura Sec-Llama su sistema live con persistenza abilitata.

**Uso:**
```bash
# Dopo boot con persistenza
sudo ./setup_persistent_env.sh
```

**Cosa installa:**
- Ollama + modello Llama 3.1 8B quantizzato (~4.5GB)
- Tool di sicurezza: nmap, masscan, wireshark, aircrack-ng, tcpdump
- Sec-Llama con tutte le dipendenze Python
- Configurazione ottimizzata per live USB

**Directory create:**
- `/root/sec-llama/` - Installazione principale
- `/opt/ollama-models/` - Modelli LLM
- `/root/sec-llama/reports/` - Report generati
- `/root/sec-llama/database/` - Database SQLite
- `/root/sec-llama/logs/` - Log operazioni

**Durata:** ~15-30 minuti (dipende da connessione internet)

---

### 3. `backup_data.sh` - Backup Dati Importanti

Backup di configurazioni, reports, database e modelli su storage esterno.

**Uso:**
```bash
# Backup su USB/disco esterno montato
sudo ./backup_data.sh /media/backup-usb

# O lasciare default (/media/backup)
sudo ./backup_data.sh
```

**Cosa viene salvato:**
- ✅ Configurazione (`config.yaml`)
- ✅ Reports generati (PDF/HTML/JSON)
- ✅ Database scansioni (SQLite)
- ✅ Training datasets
- ✅ Lista modelli custom Ollama
- ⚠️ Logs (opzionale, richiesto conferma)
- ⚠️ Modelli LLM (opzionale, richiede molto spazio)

**Output:**
- Directory: `sec-llama-backup-YYYYMMDD_HHMMSS/`
- Opzionale: archivio compresso `.tar.gz`
- File `MANIFEST.txt` con dettagli backup

**Esempio:**
```bash
# Monta disco esterno
sudo mount /dev/sdc1 /media/backup

# Esegui backup
sudo ./backup_data.sh /media/backup

# Output: /media/backup/sec-llama-backup-20241113_154523/
```

---

### 4. `external_models_storage.sh` - Gestione Storage Esterno

Configura disco/SSD esterno per modelli Ollama (risparmia spazio su USB live).

**Uso:**

**Modalità Interattiva:**
```bash
sudo ./external_models_storage.sh
# Segui menu interattivo
```

**Modalità Automatica:**
```bash
# Setup diretto con device specifico
sudo ./external_models_storage.sh sdc1
```

**Funzionalità:**
1. **Rileva storage esterno** - Scansione dispositivi disponibili
2. **Setup storage** - Monta e configura device per Ollama
3. **Migra modelli** - Sposta modelli esistenti su storage esterno
4. **Auto-mount** - Configura mount automatico al boot (systemd)
5. **Verifica config** - Controlla configurazione attuale

**Vantaggi:**
- 💾 Risparmia spazio su USB persistente
- ⚡ SSD esterno = performance migliori
- 🔄 Modelli accessibili da più sistemi
- 📦 Facilita backup di modelli grandi

**Esempio Workflow:**
```bash
# 1. Collega SSD esterno USB-C da 256GB

# 2. Esegui script
sudo ./external_models_storage.sh

# 3. Menu -> Opzione 1 (Rileva storage)
# Output: Mostra /dev/sdc1 (256GB)

# 4. Inserisci: sdc1

# 5. Conferma migrazione modelli esistenti

# 6. Configura auto-mount (opzionale)

# ✓ Fatto! Modelli ora su /mnt/ollama-external/ollama-models
```

---

## 🚀 Workflow Completo

### Setup Iniziale (Una Tantum)

```bash
# === SU LINUX (per creare USB) ===

# 1. Scarica ISO Kali Linux
wget https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-live-amd64.iso

# 2. Identifica USB (ATTENZIONE!)
lsblk

# 3. Crea USB con persistenza (esempio: USB da 64GB)
sudo ./create_persistent_usb.sh /dev/sdb kali-linux-2024.3-live-amd64.iso 32GB

# === BOOT DA USB ===

# 4. Seleziona "Live USB Persistence" dal menu GRUB

# === DOPO BOOT ===

# 5. Clona repository
git clone https://github.com/yourusername/Sec-llama.git /root/sec-llama
cd /root/sec-llama

# 6. Esegui setup completo
sudo bash scripts/setup_persistent_env.sh

# 7. (Opzionale) Configura storage esterno per modelli
sudo bash scripts/external_models_storage.sh sdc1

# 8. Test
sec-llama --help
sec-llama network discover 192.168.1.0/24
```

### Uso Quotidiano

```bash
# Boot da USB con persistence

# Verifica Ollama attivo
ollama list

# Usa Sec-Llama normalmente
sec-llama network discover 192.168.1.0/24
sec-llama code scan /path/to/project
sec-llama pentest plan --target example.com

# Backup prima di spegnere (raccomandato)
sudo bash scripts/backup_data.sh /media/backup-usb
```

---

## 📊 Requisiti Storage

### Configurazione Minima (16GB USB)
```
├── Sistema Live: 4GB
├── Persistenza OS: 4GB
├── Sec-Llama + deps: 2GB
├── Modello LLM 8B: 5GB
└── Reports/Database: 1GB
─────────────────────────
Total: 16GB (tight!)
```

### Configurazione Raccomandata (32GB+ USB)
```
├── Sistema Live: 4GB
├── Persistenza OS: 8GB
├── Sec-Llama + deps: 2GB
├── Modello LLM 8B: 5GB
├── Reports/Database: 5GB
└── Spazio libero: 8GB
─────────────────────────
Total: 32GB
```

### Configurazione Ideale (64GB USB + SSD Esterno)
```
USB 64GB:
├── Sistema Live: 4GB
├── Persistenza OS: 16GB
├── Sec-Llama + deps: 2GB
├── Reports/Database: 20GB
└── Spazio libero: 22GB

SSD Esterno 256GB:
├── Modelli LLM (8B): 5GB
├── Modelli LLM (70B): 40GB
├── Training datasets: 20GB
├── Backup: 50GB
└── Spazio libero: 141GB
─────────────────────────
Total: 320GB storage combinato
```

---

## 🔧 Troubleshooting

### Script Non Eseguibili

```bash
chmod +x scripts/*.sh
```

### Persistenza Non Funziona

```bash
# Verifica partizione
lsblk -f | grep persistence

# Verifica file config
cat /run/live/persistence/sdb3/persistence.conf
# Dovrebbe contenere: / union

# Ricrea manualmente
sudo mount /dev/sdb3 /mnt
echo "/ union" | sudo tee /mnt/persistence.conf
sudo umount /mnt
```

### Ollama Non Parte

```bash
# Verifica processo
ps aux | grep ollama

# Riavvia manualmente
pkill ollama
export OLLAMA_MODELS=/opt/ollama-models
nohup ollama serve > /tmp/ollama.log 2>&1 &

# Verifica log
tail -f /tmp/ollama.log
```

### Storage Esterno Non Monta

```bash
# Verifica device
lsblk

# Monta manualmente
sudo mkdir -p /mnt/external
sudo mount /dev/sdc1 /mnt/external

# Verifica filesystem
sudo fsck /dev/sdc1
```

---

## 📚 Documentazione Completa

Per guida dettagliata con tutti i metodi di persistenza, vedi:
- [docs/LIVE_USB_GUIDE.md](../docs/LIVE_USB_GUIDE.md) - Guida completa live USB
- [README.md](../README.md) - Documentazione principale
- [docs/FEATURES.md](../docs/FEATURES.md) - Lista funzionalità
- [docs/TRAINING.md](../docs/TRAINING.md) - Sistema training LLM

---

## ⚠️ Note Importanti

1. **Backup Regolari:** Usa `backup_data.sh` prima di ogni shutdown
2. **Verifica Device:** Usa sempre `lsblk` prima di `create_persistent_usb.sh`
3. **Spazio:** Monitora spazio disponibile con `df -h`
4. **Performance:** SSD esterno > USB 3.0 > USB 2.0
5. **Sicurezza:** Considera crittografia LUKS per dati sensibili

---

**Supporto:** Per problemi, consulta la documentazione completa o apri una issue su GitHub.
