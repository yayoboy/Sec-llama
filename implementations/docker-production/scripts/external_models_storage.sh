#!/bin/bash
# Script per usare storage esterno per modelli Ollama
# Utile quando la USB persistente ha poco spazio

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Funzione per rilevare storage esterno
detect_external_storage() {
    print_info "Ricerca dispositivi esterni..."
    echo ""

    # Lista dispositivi block escludendo loop e dm
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,LABEL | grep -v "loop\|dm-" | grep "disk\|part"

    echo ""
    print_warning "Identificare il dispositivo esterno dalla lista sopra"
    print_warning "Esempio: sdb1, sdc1, nvme0n1p1"
}

# Funzione per configurare storage esterno
setup_external_storage() {
    local DEVICE=$1
    local MOUNT_POINT="/mnt/ollama-external"

    # Verifica device
    if [ ! -b "/dev/$DEVICE" ]; then
        print_error "Device /dev/$DEVICE non trovato"
        return 1
    fi

    # Crea mount point
    mkdir -p "$MOUNT_POINT"

    # Monta device
    print_info "Montaggio /dev/$DEVICE su $MOUNT_POINT..."
    mount "/dev/$DEVICE" "$MOUNT_POINT"

    if [ $? -eq 0 ]; then
        print_info "✓ Montaggio riuscito"
    else
        print_error "Errore durante il montaggio"
        return 1
    fi

    # Crea directory per modelli
    mkdir -p "$MOUNT_POINT/ollama-models"

    # Spazio disponibile
    AVAILABLE_SPACE=$(df -h "$MOUNT_POINT" | tail -1 | awk '{print $4}')
    print_info "Spazio disponibile: $AVAILABLE_SPACE"

    # Configura Ollama
    export OLLAMA_MODELS="$MOUNT_POINT/ollama-models"

    # Aggiungi a bashrc per persistenza
    if ! grep -q "OLLAMA_MODELS=$MOUNT_POINT/ollama-models" /root/.bashrc; then
        cat >> /root/.bashrc << EOF

# Ollama External Storage
export OLLAMA_MODELS=$MOUNT_POINT/ollama-models
EOF
        print_info "✓ Configurazione aggiunta a .bashrc"
    fi

    # Riavvia Ollama con nuova configurazione
    print_info "Riavvio Ollama..."
    pkill ollama 2>/dev/null || true
    sleep 2
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3

    print_info "✓ Setup storage esterno completato"
    print_info "Modelli verranno salvati in: $MOUNT_POINT/ollama-models"

    return 0
}

# Funzione per migrare modelli esistenti
migrate_existing_models() {
    local OLD_DIR="/opt/ollama-models"
    local NEW_DIR="/mnt/ollama-external/ollama-models"

    if [ ! -d "$OLD_DIR" ]; then
        print_info "Nessun modello esistente da migrare"
        return 0
    fi

    local MODELS_SIZE=$(du -sh "$OLD_DIR" 2>/dev/null | cut -f1)
    print_warning "Trovati modelli esistenti: $MODELS_SIZE"

    read -p "Migrare modelli su storage esterno? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Migrazione in corso... Potrebbe richiedere tempo"

        # Ferma Ollama
        pkill ollama 2>/dev/null || true
        sleep 2

        # Copia modelli
        rsync -av --progress "$OLD_DIR/" "$NEW_DIR/"

        if [ $? -eq 0 ]; then
            print_info "✓ Modelli migrati con successo"

            read -p "Eliminare modelli dalla directory originale? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -rf "$OLD_DIR"
                print_info "✓ Directory originale eliminata"
            fi
        else
            print_error "Errore durante la migrazione"
            return 1
        fi

        # Riavvia Ollama
        nohup ollama serve > /tmp/ollama.log 2>&1 &
        sleep 3
    fi

    return 0
}

# Funzione per auto-mount al boot
setup_automount() {
    local DEVICE=$1
    local UUID=$(blkid "/dev/$DEVICE" | grep -o 'UUID="[^"]*"' | cut -d'"' -f2)

    if [ -z "$UUID" ]; then
        print_error "UUID non trovato per /dev/$DEVICE"
        return 1
    fi

    print_info "UUID del dispositivo: $UUID"

    # Crea script di auto-mount
    cat > /etc/systemd/system/ollama-external-mount.service << EOF
[Unit]
Description=Mount Ollama External Storage
After=local-fs.target

[Service]
Type=oneshot
ExecStart=/bin/mount UUID=$UUID /mnt/ollama-external
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

    # Abilita servizio
    systemctl daemon-reload
    systemctl enable ollama-external-mount.service

    print_info "✓ Auto-mount configurato"
    print_info "Storage esterno verrà montato automaticamente al boot"

    return 0
}

# Menu principale
show_menu() {
    echo ""
    echo "==================================="
    echo "  Ollama External Storage Manager"
    echo "==================================="
    echo ""
    echo "1) Rileva e configura storage esterno"
    echo "2) Migra modelli esistenti su storage esterno"
    echo "3) Configura auto-mount al boot"
    echo "4) Verifica configurazione attuale"
    echo "5) Esci"
    echo ""
}

verify_config() {
    echo ""
    print_info "Configurazione Attuale:"
    echo "  OLLAMA_MODELS: ${OLLAMA_MODELS:-non configurato}"
    echo ""

    if command -v ollama &> /dev/null; then
        print_info "Modelli installati:"
        ollama list
    else
        print_warning "Ollama non installato"
    fi

    echo ""
    print_info "Storage montati:"
    df -h | grep -E "Filesystem|/mnt/|/media/"
}

# Main
if [ "$EUID" -ne 0 ]; then
    print_error "Questo script deve essere eseguito come root"
    exit 1
fi

# Se passato device come argomento, setup diretto
if [ -n "$1" ]; then
    print_info "Setup storage esterno su /dev/$1"
    setup_external_storage "$1"
    migrate_existing_models

    read -p "Configurare auto-mount? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_automount "$1"
    fi

    exit 0
fi

# Menu interattivo
while true; do
    show_menu
    read -p "Scegli opzione: " choice

    case $choice in
        1)
            detect_external_storage
            echo ""
            read -p "Inserisci device (es: sdb1): " device
            if [ -n "$device" ]; then
                setup_external_storage "$device"
            fi
            ;;
        2)
            migrate_existing_models
            ;;
        3)
            read -p "Inserisci device da auto-montare (es: sdb1): " device
            if [ -n "$device" ]; then
                setup_automount "$device"
            fi
            ;;
        4)
            verify_config
            ;;
        5)
            print_info "Uscita"
            exit 0
            ;;
        *)
            print_error "Opzione non valida"
            ;;
    esac

    echo ""
    read -p "Premi ENTER per continuare..."
done
