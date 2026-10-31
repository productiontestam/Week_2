FROM alpine:3.24

RUN apk add --no-cache \
    zabbix-agent2 \
    net-snmp \
    net-snmp-tools

COPY snmpd.conf /etc/snmp/snmpd.conf
COPY zabbix_agent2.conf /etc/zabbix/zabbix_agent2.conf
COPY start-services.sh /usr/local/bin/start-services.sh

RUN chmod +x /usr/local/bin/start-services.sh

EXPOSE 161/udp 10050/tcp

ENTRYPOINT ["/usr/local/bin/start-services.sh"]
