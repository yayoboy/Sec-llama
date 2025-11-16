#!/bin/bash
# Script per backup dei dati importanti da Live USB
# Utile per salvare reports, database, modelli custom su storage esterno

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[====== $1 ======]${NC}"
}

# Configurazione
SEC_LLAMA_DIR="/root/sec-llama"
OLLAMA_MODELS_DIR="/opt/ollama-models"
BACKUP_DEST=${1:-"/media/backup"}

# Crea timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$BACKUP_DEST/sec-llama-backup-$TIMESTAMP"

if [ ! -d "$BACKUP_DEST" ]; then
    print_warning "Directory di destinazione $BACKUP_DEST non trovata"
    echo "Uso: $0 <backup_destination>"
    echo "Esempio: $0 /media/usb-backup"
    echo ""
    echo "Monta prima il dispositivo esterno:"
    echo "  sudo mount /dev/sdb1 /media/backup"
    exit 1
fi

print_section "Backup Sec-Llama Data"
print_info "Destinazione: $BACKUP_DIR"

mkdir -p "$BACKUP_DIR"

# 1. Backup configurazione
print_info "Backup configurazione..."
if [ -f "$SEC_LLAMA_DIR/config/config.yaml" ]; then
    cp "$SEC_LLAMA_DIR/config/config.yaml" "$BACKUP_DIR/"
    print_info "✓ Configurazione salvata"
fi

# 2. Backup reports
print_info "Backup reports..."
if [ -d "$SEC_LLAMA_DIR/reports" ]; then
    REPORTS_COUNT=$(find "$SEC_LLAMA_DIR/reports" -type f | wc -l)
    if [ $REPORTS_COUNT -gt 0 ]; then
        cp -r "$SEC_LLAMA_DIR/reports" "$BACKUP_DIR/"
        print_info "✓ $REPORTS_COUNT reports salvati"
    else
        print_info "Nessun report trovato"
    fi
fi

# 3. Backup database
print_info "Backup database..."
if [ -d "$SEC_LLAMA_DIR/database" ]; then
    cp -r "$SEC_LLAMA_DIR/database" "$BACKUP_DIR/"
    print_info "✓ Database salvato"
fi

# 4. Backup logs (opzionale)
read -p "Backup logs? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$SEC_LLAMA_DIR/logs" ]; then
        cp -r "$SEC_LLAMA_DIR/logs" "$BACKUP_DIR/"
        print_info "✓ Logs salvati"
    fi
fi

# 5. Backup modelli custom
print_info "Verifica modelli custom Ollama..."
CUSTOM_MODELS=$(ollama list | grep -v "NAME" | grep -v "llama" | grep -v "mistral" | wc -l)

if [ $CUSTOM_MODELS -gt 0 ]; then
    print_warning "Trovati $CUSTOM_MODELS modelli custom"
    read -p "Backup modelli custom? Richiede molto spazio (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "$BACKUP_DIR/custom-models"

        # Lista modelli custom
        ollama list | grep -v "NAME" | grep -v "llama3.1:8b" | awk '{print $1}' > "$BACKUP_DIR/custom-models/model-list.txt"

        # Backup Modelfile se esistono
        if [ -d "$SEC_LLAMA_DIR/models" ]; then
            cp -r "$SEC_LLAMA_DIR/models" "$BACKUP_DIR/custom-models/"
        fi

        print_info "✓ Lista modelli custom salvata"
        print_warning "Per backup completo, copiare manualmente: $OLLAMA_MODELS_DIR"
    fi
fi

# 6. Backup training datasets
if [ -d "$SEC_LLAMA_DIR/datasets" ]; then
    DATASETS_COUNT=$(find "$SEC_LLAMA_DIR/datasets" -name "*.json" | wc -l)
    if [ $DATASETS_COUNT -gt 0 ]; then
        print_info "Backup $DATASETS_COUNT training datasets..."
        cp -r "$SEC_LLAMA_DIR/datasets" "$BACKUP_DIR/"
        print_info "✓ Datasets salvati"
    fi
fi

# 7. Crea manifesto backup
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
Sec-Llama Backup
================
Data: $(date)
Hostname: $(hostname)
User: $(whoami)

Contenuto:
$(tree -L 2 "$BACKUP_DIR" 2>/dev/null || find "$BACKUP_DIR" -maxdepth 2 -type f)

Spazio occupato:
$(du -sh "$BACKUP_DIR")

Per ripristinare:
1. Montare USB con persistenza
2. Eseguire setup_persistent_env.sh
3. Copiare config.yaml in /root/sec-llama/config/
4. Copiare reports, database, logs in /root/sec-llama/
EOF

# Calcola dimensione totale
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

print_section "Backup Completato"
print_info "Dimensione totale: $BACKUP_SIZE"
print_info "Percorso: $BACKUP_DIR"
print_info ""
print_info "Contenuto backup:"
ls -lah "$BACKUP_DIR"

# Opzione: crea archivio compresso
echo ""
read -p "Creare archivio compresso? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Compressione in corso..."
    tar -czf "$BACKUP_DIR.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"
    COMPRESSED_SIZE=$(du -sh "$BACKUP_DIR.tar.gz" | cut -f1)
    print_info "✓ Archivio creato: $BACKUP_DIR.tar.gz ($COMPRESSED_SIZE)"

    read -p "Eliminare directory non compressa? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$BACKUP_DIR"
        print_info "Directory rimossa, archivio: $BACKUP_DIR.tar.gz"
    fi
fi

print_info ""
print_info "Backup completato con successo! ✓"
