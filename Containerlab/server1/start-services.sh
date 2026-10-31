#!/bin/sh
set -eu

: "${SNMP_COMMUNITY:?SNMP_COMMUNITY environment variable is required}"

sed "s|\${SNMP_COMMUNITY}|${SNMP_COMMUNITY}|g" \
    /etc/snmp/snmpd.conf > /tmp/snmpd.conf

snmpd -f -Lo -C -c /tmp/snmpd.conf &
SNMP_PID=$!

zabbix_agent2 -c /etc/zabbix/zabbix_agent2.conf &
ZABBIX_PID=$!

cleanup() {
    kill "$SNMP_PID" "$ZABBIX_PID" 2>/dev/null || true
    wait "$SNMP_PID" "$ZABBIX_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

while :; do
    if ! kill -0 "$SNMP_PID" 2>/dev/null; then
        echo "SNMP service stopped unexpectedly."
        exit 1
    fi

    if ! kill -0 "$ZABBIX_PID" 2>/dev/null; then
        echo "Zabbix Agent2 stopped unexpectedly."
        exit 1
    fi

    sleep 2
done
