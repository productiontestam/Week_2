"""Lab-only: read LLDP neighbors over SNMP and ingest cables into NetBox through Diode."""
import os
import subprocess
import sys


RUNNER = ["docker", "exec", "clab-my-simple-lab-server1"]
DEVICES = {"router1": "10.10.10.2", "switch1": "10.10.10.4", "server1": "10.10.10.3"}
COMMUNITY = os.environ["SNMP_COMMUNITY"]
IF_DESCR = ".1.3.6.1.2.1.2.2.1.2"
REM_PORT_DESC = ".1.0.8802.1.1.2.1.4.1.1.8"
REM_SYS_NAME = ".1.0.8802.1.1.2.1.4.1.1.9"


def walk(host, prefix):
    cmd = RUNNER + ["snmpwalk", "-v2c", "-c", COMMUNITY, "-On", "-Oq", host, prefix]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    base = prefix.lstrip(".") + "."
    rows = {}
    for line in out.splitlines():
        key, _, value = line.partition(" ")
        key = key.lstrip(".")
        if key.startswith(base):
            rows[key[len(base):]] = value.strip().strip('"')
    return rows


def links_for(device, host):
    ifaces = walk(host, IF_DESCR)
    sys_names = walk(host, REM_SYS_NAME)
    port_descs = walk(host, REM_PORT_DESC)
    found = []
    for suffix, remote_device in sys_names.items():
        _, local_port, _ = suffix.split(".")
        found.append(((device, ifaces.get(local_port)), (remote_device, port_descs.get(suffix))))
    return found


def terminal(end):
    interface = Interface(device=Device(name=end[0], site="undefined"), name=end[1])
    return [GenericObject(object_interface=interface)]


planned = {}
for device, host in DEVICES.items():
    for a, b in links_for(device, host):
        if None in a or None in b:
            print("skipped incomplete neighbor:", a, b)
            continue
        planned[tuple(sorted([a, b]))] = (a, b)

for a, b in planned.values():
    print(f"{a[0]}:{a[1]} <-> {b[0]}:{b[1]}")
print(f"{len(planned)} cable(s) planned")

if "--apply" in sys.argv:
    from netboxlabs.diode.sdk import DiodeClient
    from netboxlabs.diode.sdk.ingester import Cable, Device, Entity, GenericObject, Interface

    entities = [
        Entity(cable=Cable(a_terminations=terminal(a), b_terminations=terminal(b)))
        for a, b in planned.values()
    ]
    with DiodeClient(
        target="grpc://192.168.1.102:8080/diode",
        app_name="lab-lldp-cables",
        app_version="0.1.0",
        client_id=os.environ["DIODE_CLIENT_ID"],
        client_secret=os.environ["DIODE_CLIENT_SECRET"],
    ) as client:
        print(client.ingest(entities=entities))
