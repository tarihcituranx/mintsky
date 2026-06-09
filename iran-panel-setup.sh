#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_ok()   { echo -e "${GREEN}[OK] $1${NC}"; }
print_err()  { echo -e "${RED}[HATA] $1${NC}"; }
print_info() { echo -e "${BLUE}[->] $1${NC}"; }

echo ""
echo "======================================"
echo "   3X-UI Panel Otomatik Ayar Script"
echo "======================================"
echo ""

apt-get install curl jq -y -qq
print_ok "Gerekli araçlar hazır."
echo ""

PANEL_PORT="47821"
PANEL_PATH="jW6EEntoNtDlxylgiT"
PANEL_USER="48tSmIZiVu"
PANEL_URL="http://localhost:${PANEL_PORT}/${PANEL_PATH}"
COOKIE_FILE="/tmp/xui_cookie.txt"

read -s -p "Panel sifrenizi girin: " PANEL_PASS
echo ""
echo ""

print_info "Baglaniyor: $PANEL_URL"

LOGIN=$(curl -s -c "$COOKIE_FILE" \
    -X POST "${PANEL_URL}/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${PANEL_USER}&password=${PANEL_PASS}")

if echo "$LOGIN" | grep -q '"success":true'; then
    print_ok "Giris basarili!"
else
    print_err "Giris basarisiz!"
    echo "Cevap: $LOGIN"
    rm -f "$COOKIE_FILE"
    exit 1
fi

echo ""
print_info "Routing kurallari ayarlaniyor..."

ROUTING='{"domainStrategy":"IPIfNonMatch","rules":[{"type":"field","outboundTag":"block","domain":["ext:geosite_IR.dat:category-ads-all","ext:geosite_IR.dat:malware","ext:geosite_IR.dat:phishing"]},{"type":"field","outboundTag":"direct","domain":["ext:geosite_IR.dat:ir"]},{"type":"field","outboundTag":"direct","ip":["ext:geoip_IR.dat:ir","geoip:private"]}]}'

UPDATE=$(curl -s -b "$COOKIE_FILE" \
    -X POST "${PANEL_URL}/xui/setting/update" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "routingConfig=${ROUTING}")

if echo "$UPDATE" | grep -q '"success":true'; then
    print_ok "Routing kurallari eklendi!"
else
    print_info "API yaniti: $UPDATE"
    print_info "Direkt config yontemi deneniyor..."

    CONFIG_PATH="/usr/local/x-ui/bin/config.json"
    if [ -f "$CONFIG_PATH" ]; then
        cp "$CONFIG_PATH" "${CONFIG_PATH}.backup"
        print_ok "Yedek alindi."
        jq '.routing = {"domainStrategy":"IPIfNonMatch","rules":[{"type":"field","outboundTag":"block","domain":["ext:geosite_IR.dat:category-ads-all","ext:geosite_IR.dat:malware","ext:geosite_IR.dat:phishing"]},{"type":"field","outboundTag":"direct","domain":["ext:geosite_IR.dat:ir"]},{"type":"field","outboundTag":"direct","ip":["ext:geoip_IR.dat:ir","geoip:private"]}]}' "$CONFIG_PATH" > /tmp/new_config.json
        mv /tmp/new_config.json "$CONFIG_PATH"
        print_ok "Config dosyasi guncellendi."
    else
        print_err "Config bulunamadi: $CONFIG_PATH"
    fi
fi

echo ""
print_info "Servis yeniden baslatiliyor..."
systemctl restart x-ui
sleep 2

if systemctl is-active --quiet x-ui; then
    print_ok "x-ui calisiyor!"
else
    print_err "x-ui baslanamadi! Kontrol: systemctl status x-ui"
fi

rm -f "$COOKIE_FILE"

echo ""
echo "======================================"
echo "           TAMAMLANDI"
echo "======================================"
echo ""
echo "  - Iran siteleri direkt baglanir"
echo "  - Reklam/malware engellendi"
echo "  - Servis yeniden baslatildi"
echo ""
