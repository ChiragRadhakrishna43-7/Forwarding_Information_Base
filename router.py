# Router simulator in a network
# To exercise routing algorithms
#
# Sin-Yaw Wang <swang24@scu.edu
#

# "links": routers directly connected, with a link cost
# "network" is the network that has all the routers in the universe

import json
import logging


class Router:
    # initialize per router variables
    def __init__(self, nm):
        self.name = nm  # name of the router
        self.links = {}  # a dictionary
        self.fib = {}  # FIB data structure for each router.

    def addLink(self, l, c):
        self.links[l] = c
        """
        Initialize fib table with directly connected neighbors.
        Destination initially is empty, next_hop are the directly connected neighbors of the router.
        """
        self.fib[l] = ('', l, c)

    def updateFIB(self, destination, next_hop, cost):
        """
        Update FIB:
        Each router's FIB in the path computed by Dijkstra Algorithm is updated.
        (Destination, next_hop, total_cost): where destination is the destination router to which the packet should be ultimately delivered to,
                                             next hop is to which router the packet is forwarded to,
                                             total_cost is total cost to reach the packet to the destination.
        """
        logging.info(f'Updated FIB for {self.name}.')
        self.fib[destination] = (destination, next_hop, cost)

    def sendData(self, dest, data):
        """
        Encapsulate packet and forward packet either to the destination or next router in path if destined router is present in the FIB.
        """
        if dest in self.fib:
            dest_router = self.fib[dest][1]
            packet = self.encapsulate(dest, data)
            if dest_router:
                logging.info(f"{self.name} forwarding data packet to {dest_router.name}.")
                dest_router.recvData(self.name, packet)
        else:
            logging.info(f"No entry for {dest} in FIB of {self.name}.")
            self.dropPkt(dest)

    def recvData(self, source, packet):
        """
        Unpack the packet and check if the packet has reached the destination.
        If destination reached, accept the packet.

        Else, log the event that the router has received the packet from the sender.
        Then, forward the packet to the next hop.
        """
        header, data = self.unpack(packet)
        if header['destination'] == self.name:
            self.acceptData(source, data)
        else:
            logging.info(f"Router {self.name} received packet from {source}.")
            self.sendData(header['destination'], data)
                   
    def encapsulate(self, destination, data):
        return json.dumps({'header': {'destination': destination}, 'data': data})
    
    def unpack(self, packet):
        packet = json.loads(packet)
        return packet['header'], packet['data']

    def dropPkt(self, destination):
        """
        Log the packet drop.
        """
        logging.info(f"Router {self.name} dropped packet to be reached to {destination}.")

    def acceptData(self, source, data):
        """
        If destination has been reached, the packet is accepted.
        Log the discard packet event at the destination, indicating that the packet has been received and data has been read at the destination.
        """
        logging.info(f"Destination reached as router {self.name} accepted data packet from {source}. Data received is as follows: {data}.")
        logging.info(f"Calling discardPkt() to discard the packet as destination has been reached.")
        self.discardPkt()

    def discardPkt(self):
        logging.info(f"Packet has reached destination {self.name}. Discarding data packet.")
        logging.info("Packet discarded.")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        str_ = '{{"Router": "{}", '.format(self.name)
        if len(self.links) > 0:
            str_ += '"Links": {'
            str_ += json.dumps(self.links)
            str_ += '}'
        str_ += '}'
        return str_
