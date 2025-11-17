# 🐳 Docker Desktop Deployment Guide

Guida completa per deployare Sec-Llama su **Docker Desktop** (Windows/Mac/Linux Desktop).

---

## 📋 Prerequisiti

### 1. Docker Desktop Installato

**Download:**
- **Windows/Mac**: https://www.docker.com/products/docker-desktop
- **Linux**: https://docs.docker.com/desktop/install/linux-install/

**Requisiti Sistema:**
- **Windows**: Windows 10 64-bit Pro/Enterprise/Education oppure Home con WSL 2
- **Mac**: macOS 11 (Big Sur) o più recente
- **RAM**: Minimo 8GB (consigliato 16GB)
- **Disk**: 20GB liberi
- **CPU**: Virtualizzazione abilitata nel BIOS

### 2. Verifica Installazione

Apri terminale/PowerShell e verifica:

```bash
# Verifica Docker
docker --version
# Output: Docker version 24.x.x

# Verifica Docker Compose
docker compose version
# Output: Docker Compose version v2.x.x

# Test Docker
docker run hello-world
```

### 3. Configurazione Docker Desktop

#### Windows

1. **Abilita WSL 2** (se non già fatto):
   ```powershell
   # In PowerShell Administrator
   wsl --install
   wsl --set-default-version 2
   ```

2. **Docker Desktop Settings**:
   - Open Docker Desktop
   - Settings → General → "Use WSL 2 based engine" ✓
   - Settings → Resources → WSL Integration → Enable your distro

#### Mac

1. **Docker Desktop Settings**:
   - Open Docker Desktop
   - Settings → Resources:
     - CPUs: 4+ cores
     - Memory: 8+ GB
     - Swap: 2+ GB
     - Disk image size: 60+ GB

#### Linux

1. **Post-install steps**:
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker

   # Start Docker Desktop
   systemctl --user start docker-desktop
   ```

---

## 🚀 Deploy con Docker Desktop

### Step 1: Prepara il Progetto

```bash
# Clone repository (o scarica ZIP)
git clone https://github.com/yayoboy/Sec-llama.git
cd Sec-llama

# Oppure se hai già i file:
cd path/to/Sec-llama
```

### Step 2: Configura Environment

```bash
# Copia template
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env

# Modifica .env con il tuo editor preferito
```

#### Windows - Notepad
```powershell
notepad .env
```

#### Mac - TextEdit
```bash
open -a TextEdit .env
```

#### Linux - nano/vim
```bash
nano .env
# oppure
code .env  # se hai VS Code
```

### Step 3: Modifica .env - Valori Obbligatori

**⚠️ IMPORTANTE: Modifica questi valori!**

```bash
# === DATABASE ===
POSTGRES_PASSWORD=TuaPasswordSicura123!

# === REDIS ===
REDIS_PASSWORD=TuaRedisPassword456!

# === LLM (Sostituisci IP con il tuo PC Ollama!) ===
OLLAMA_HOST=http://192.168.1.100:11434

# === SECURITY (Genera con comando sotto) ===
SECRET_KEY=chiave_generata_random_32_caratteri
JWT_SECRET_KEY=altra_chiave_generata_random_32_caratteri

# === ADMIN ===
ADMIN_PASSWORD=CambiamiAlPrimoLogin!
```

**Genera chiavi sicure:**

```bash
# Mac/Linux:
openssl rand -hex 32

# Windows (PowerShell):
# Installa prima: choco install openssl
openssl rand -hex 32

# Oppure online: https://www.random.org/strings/
# Genera 2 stringhe da 64 caratteri
```

### Step 4: Valida Configurazione

```bash
# Mac/Linux:
./validate-env.sh

# Windows (Git Bash):
bash validate-env.sh

# Windows (PowerShell) - manualmente:
Get-Content .env | Select-String "CHANGE_ME"
# Se restituisce risultati, devi ancora modificare i valori!
```

### Step 5: Avvia con Docker Desktop

#### Metodo 1: Docker Compose CLI

```bash
# Build e start
docker compose up -d

# Segui i logs
docker compose logs -f web-ui

# Verifica status
docker compose ps
```

#### Metodo 2: Docker Desktop GUI

1. **Apri Docker Desktop**

2. **Containers**:
   - Verifica che Docker Desktop sia running (icona verde)

3. **Terminal integrato**:
   ```bash
   cd /path/to/Sec-llama
   docker compose up -d
   ```

4. **Monitoring**:
   - Vai su "Containers" tab
   - Dovresti vedere 3 container:
     - `sec-llama-postgres` (verde)
     - `sec-llama-redis` (verde)
     - `sec-llama-web-ui` (verde)

5. **View Logs**:
   - Click su container → "View Details" → "Logs"

---

## ✅ Verifica Deployment

### 1. Check Container Status

**Docker Desktop GUI:**
- Containers → Tutti e 3 devono essere "Running" (verde)

**CLI:**
```bash
docker compose ps

# Output atteso:
# NAME                    STATUS              PORTS
# sec-llama-postgres      Up (healthy)        5432/tcp
# sec-llama-redis         Up (healthy)        6379/tcp
# sec-llama-web-ui        Up (healthy)        0.0.0.0:8080->8080/tcp
```

### 2. Check Logs

```bash
# Web UI logs
docker compose logs web-ui

# Cerca:
# "Application startup complete"
# "Uvicorn running on http://0.0.0.0:8080"
```

### 3. Test Web UI

Apri browser e vai a:
```
http://localhost:8080
```

**Login:**
- Username: `admin`
- Password: (quella impostata in .env)

### 4. Test API Health

```bash
# Mac/Linux:
curl http://localhost:8080/api/health

# Windows (PowerShell):
Invoke-WebRequest http://localhost:8080/api/health

# Output atteso (JSON):
# {"status":"healthy","database":"connected","redis":"connected"}
```

---

## 🛠️ Gestione con Docker Desktop

### Start/Stop Containers

**GUI:**
- Containers → Seleziona stack → Play/Stop button

**CLI:**
```bash
# Start
docker compose up -d

# Stop
docker compose down

# Restart
docker compose restart

# Stop singolo container
docker compose stop web-ui
docker compose start web-ui
```

### View Logs

**GUI:**
- Containers → Click container → View Details → Logs tab

**CLI:**
```bash
# Tutti i logs
docker compose logs -f

# Solo web-ui
docker compose logs -f web-ui

# Ultime 100 righe
docker compose logs --tail=100 web-ui
```

### Console/Shell Access

**GUI:**
- Containers → Click container → "CLI" button

**CLI:**
```bash
# Web UI shell
docker compose exec web-ui /bin/bash

# PostgreSQL shell
docker compose exec postgres psql -U sec_llama -d sec_llama

# Redis shell
docker compose exec redis redis-cli -a your_redis_password
```

### Resource Monitoring

**GUI:**
- Containers → Click container → Stats tab
  - CPU %
  - Memory usage
  - Network I/O
  - Disk I/O

**CLI:**
```bash
docker stats
```

---

## 🔧 Troubleshooting Docker Desktop

### Container Non Si Avvia

**Problema**: Container in stato "Exited" o "Restarting"

**Soluzione**:

1. **Check logs**:
   ```bash
   docker compose logs web-ui
   ```

2. **Verifica .env**:
   ```bash
   # Mac/Linux:
   cat .env | grep -v "^#" | grep -v "^$"

   # Windows:
   Get-Content .env | Where-Object {$_ -notmatch '^#' -and $_ -notmatch '^$'}
   ```

3. **Rebuild container**:
   ```bash
   docker compose down
   docker compose build --no-cache
   docker compose up -d
   ```

### Port Already in Use

**Problema**: "Error: port 8080 already allocated"

**Windows - Trova processo**:
```powershell
# Trova processo che usa porta 8080
netstat -ano | findstr :8080

# Uccidi processo (sostituisci PID)
taskkill /PID <PID> /F
```

**Mac - Trova processo**:
```bash
# Trova processo
lsof -i :8080

# Uccidi processo
kill -9 <PID>
```

**Soluzione alternativa**: Cambia porta in `.env`:
```bash
WEB_UI_PORT=8081
```

### Volume Permission Issues (Linux/Mac)

**Problema**: Permission denied su `./data/`

**Soluzione**:
```bash
# Linux/Mac:
sudo chown -R $(id -u):$(id -g) ./data

# Verifica permissions
ls -la ./data/
```

### WSL 2 Issues (Windows)

**Problema**: "WSL 2 installation is incomplete"

**Soluzione**:
```powershell
# In PowerShell Administrator

# Update WSL
wsl --update

# Set WSL 2 as default
wsl --set-default-version 2

# Restart Docker Desktop
```

### Docker Desktop Won't Start (Mac)

**Problema**: "Docker Desktop failed to start"

**Soluzione**:

1. **Reset Docker Desktop**:
   - Troubleshoot → Reset to factory defaults

2. **Clear Docker data**:
   ```bash
   rm -rf ~/Library/Containers/com.docker.docker
   ```

3. **Reinstall Docker Desktop**

### Build Errors

**Problema**: "Error building image"

**Soluzione**:

1. **Clear build cache**:
   ```bash
   docker builder prune -a
   ```

2. **Rebuild without cache**:
   ```bash
   docker compose build --no-cache --pull
   ```

3. **Check disk space**:
   ```bash
   docker system df
   docker system prune -a  # WARNING: removes all unused data
   ```

---

## 💾 Data Persistence

### Backup Volumes

```bash
# Backup PostgreSQL
docker compose exec postgres pg_dump -U sec_llama sec_llama > backup_$(date +%Y%m%d).sql

# Backup all volumes
docker run --rm \
  -v sec-llama-postgres-data:/source \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_$(date +%Y%m%d).tar.gz -C /source .
```

### Restore Volumes

```bash
# Restore PostgreSQL
cat backup_20250116.sql | docker compose exec -T postgres psql -U sec_llama -d sec_llama
```

### Reset Everything

**⚠️ WARNING: Cancella tutti i dati!**

```bash
# Stop e rimuovi tutto
docker compose down -v

# Rimuovi volumi named
docker volume rm sec-llama-postgres-data sec-llama-redis-data

# Pulisci dati locali
rm -rf ./data/*

# Restart fresh
docker compose up -d
```

---

## 🔄 Update Containers

### Update Immagini

```bash
# Pull nuove versioni
docker compose pull

# Rebuild e restart
docker compose up -d --build
```

### Update Codice

```bash
# Pull latest code
git pull

# Rebuild
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 📊 Performance Tuning Docker Desktop

### Windows (WSL 2)

**`.wslconfig` file** in `C:\Users\<username>\.wslconfig`:

```ini
[wsl2]
memory=8GB           # Limits VM memory
processors=4         # Limits VM cores
swap=4GB            # VM swap size
localhostForwarding=true
```

**Restart WSL**:
```powershell
wsl --shutdown
# Restart Docker Desktop
```

### Mac

**Docker Desktop Settings → Resources**:
- **CPUs**: 4-8 cores
- **Memory**: 8-16 GB
- **Swap**: 2-4 GB
- **Disk**: 60+ GB

**Enable VirtioFS** (faster file sharing):
- Settings → General → "VirtioFS" ✓

### All Platforms

**Settings → Docker Engine** - Add:

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "20GB"
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
```

---

## 📚 Shortcuts Docker Desktop

### Comandi Rapidi

```bash
# Status quick
docker compose ps

# Logs tail (ultime righe)
docker compose logs --tail=50 -f

# Restart rapido
docker compose restart web-ui

# Shell rapida
docker compose exec web-ui bash

# Clean tutto
docker system prune -a --volumes
```

### GUI Features

1. **Dev Environments** (Compose file preview)
2. **Extensions** (Database viewers, etc.)
3. **Volumes** viewer
4. **Images** management
5. **Integrated terminal**

---

## 🆘 Supporto

### Log Locations

**Docker Desktop Logs:**
- **Windows**: `%APPDATA%\Docker\log\`
- **Mac**: `~/Library/Containers/com.docker.docker/Data/log/`
- **Linux**: `~/.docker/desktop/log/`

**Container Logs:**
```bash
docker compose logs > full_logs_$(date +%Y%m%d).txt
```

### Diagnostics

**Docker Desktop**:
- Troubleshoot → Run Diagnostics
- Upload diagnostics ID per supporto

### Community

- **Docker Desktop Issues**: https://github.com/docker/for-mac/issues
- **Sec-Llama Issues**: https://github.com/yayoboy/Sec-llama/issues

---

**Buon deploy su Docker Desktop! 🐳🚀**
