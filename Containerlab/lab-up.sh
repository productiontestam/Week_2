#!/bin/bash
cd ~/containerlab
sudo containerlab deploy -t containerlab.clab.yml --reconfigure
docker exec clab-my-simple-lab-router1 ip route replace default via 10.10.10.1
docker exec clab-my-simple-lab-server1 ip route replace default via 10.10.10.1
for n in router1 server1 switch1; do
  docker cp scripts/lab-setup.sh clab-my-simple-lab-$n:/lab-setup.sh
  docker exec clab-my-simple-lab-$n sh /lab-setup.sh $n
done
docker exec clab-my-simple-lab-server1 ip route replace default via 192.168.20.1
echo "lab is up"
