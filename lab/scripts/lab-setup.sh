#!/bin/sh
NODE="$1"
apk info -e net-snmp net-snmp-tools lldpd >/dev/null 2>&1 || apk add --no-cache net-snmp net-snmp-tools lldpd
mkdir -p /etc/snmp /var/agentx
cat > /etc/snmp/snmpd.conf << EOF
agentAddress udp:161
rocommunity labro 10.10.10.0/24
rocommunity labro 127.0.0.1
sysName ${NODE}
sysLocation my-simple-lab
master agentx
EOF
pkill snmpd
pkill lldpd
sleep 1
snmpd -C -c /etc/snmp/snmpd.conf -Lf /var/log/snmpd.log -p /var/run/snmpd.pid </dev/null >/dev/null 2>&1
lldpd -x -I 'eth*,!eth0' </dev/null >/dev/null 2>&1
sleep 3
lldpcli configure system hostname "${NODE}"
echo "setup done ${NODE}"
