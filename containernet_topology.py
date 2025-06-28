from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink

def create_partitioned_topo():
    net = Containernet(controller=Controller)
    net.addController('c0')

    d1 = net.addDocker('d1', ip='10.0.0.251', dimage="my_tree_server", volumes=["/home/blackdragoon/containernet_project:/app"])
    d2 = net.addDocker('d2', ip='10.0.0.252', dimage="my_tree_server", volumes=["/home/blackdragoon/containernet_project:/app"])
    d3 = net.addDocker('d3', ip='10.0.0.253', dimage="my_tree_server", volumes=["/home/blackdragoon/containernet_project:/app"])

    s1 = net.addSwitch('s1')
    net.addLink(d1, s1, cls=TCLink)
    net.addLink(d2, s1, cls=TCLink)
    net.addLink(d3, s1, cls=TCLink)

    net.start()

    # Start servers in containers
    d1.cmd('python3 /app/server_partition.py --partition 0 --next 10.0.0.252:5001 &')
    d2.cmd('python3 /app/server_partition.py --partition 1 --next 10.0.0.253:5002 &')
    d3.cmd('python3 /app/server_partition.py --partition 2 --next none &')

    print("Topology is up. Test by sending input to d1.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    from mininet.cli import CLI
    create_partitioned_topo()

