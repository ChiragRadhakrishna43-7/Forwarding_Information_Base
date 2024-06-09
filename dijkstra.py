# CSEN 233 Homework 8:
# Chirag Radhakrishna (cradhakrishna@scu.edu) SCU ID: 07700009612
# Dijkstra Algorithm Implementation with FIB
# ---------------------------------------------------------------

from netemulate import netEmulator
from queue import PriorityQueue
from router import Router
import logging
import random
import sys


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s -%(message)s', filename = "csen233hw8RadhakrishnaChirag.logs", filemode = "a")
logger = logging.getLogger(__name__)

class Dijkstra(netEmulator):
    def __init__(self):
        super().__init__()

    def dijkstra(self, r1, r2):
        """
        Computes the shortest path between the two given routers r1 and r2.
        Returns the shortest path and the cost of that respective path.
        """
        path = []
        logger.info("Obtaining the names of the two routers.")
        pair = [r for r in self.routers if r.name == r1 or r.name == r2]
        if len(pair) != 2:
            logger.error(f"Invalid pair of routers: {pair}.")
            return None, None
        src, dest = pair
        dist = {router.name: float('inf') for router in self.routers}
        dist[src.name] = 0
        pr_queue = PriorityQueue()
        pr_queue.put((0, src.name))
        prev = {router.name: None for router in self.routers}
        while not pr_queue.empty():
            curr_dist, curr_node = pr_queue.get()
            if curr_node == dest.name:
                logger.info(f"Shortest path found between {r1} and {r2}.")
                while prev[curr_node]:
                    path.append(curr_node)
                    curr_node = prev[curr_node]
                path.append(src.name)
                path.reverse() if path[-1] == r1 else None
                return path, dist[dest.name]
            for router in self.routers:
                if router.name == curr_node:
                    for neighbor_node, weight in router.links.items():
                        distance = curr_dist + weight
                        if distance < dist[neighbor_node]:
                            dist[neighbor_node] = distance
                            prev[neighbor_node] = curr_node
                            pr_queue.put((distance, neighbor_node))
        
        return path, None

    def get_router_by_name(self, name):
        """
        Simply return the name of the router.
        """
        for router in self.routers:
            if router.name == name:
                return router
        return None

# MAIN 
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Need topology file.')
        sys.exit()
    if len(sys.argv) <= 4:
        print('Need the two routers and an invalid router (Router that is not in the list of routers present in net.json file.')
        print('Usage Example: python dijkstra.py net.json R01 R02 R21')
        sys.exit()
    net = Dijkstra()
    net.rtInit(sys.argv[1])
    print('net has {} routers'.format(len(net.routers)))
    r1 = sys.argv[2]
    r2 = sys.argv[3]
    r3 = sys.argv[4]
    path, total = net.dijkstra(r1, r2)
    logger.info(f"Shortest path between {r1} and {r2} is {path}.")

    """
    The dijkstra() method returns the path and the total cost of the path.
    Iterate over the path, and update the FIB for every router encountered in the path till the destination.
    """
    for i in range(len(path) - 1):
        curr_router = net.get_router_by_name(path[i])
        next_router = net.get_router_by_name(path[i + 1])
        logger.info(f"Updating FIB entry for {curr_router.name} as ({r2}, {next_router.name}, {total}).")
        curr_router.updateFIB(r2, next_router, total)
        total = total - curr_router.links[next_router.name]
    """
    POSITIVE CASE
    -------------
    The FIB for the routers across the path are updated.
    Packet is sent from r1 to r2.
    """
    logger.info("POSITIVE CASE:")
    logger.info("--------------")
    data = "-->[Test data from {} to {}]".format(r1, r2)
    net.get_router_by_name(r1).sendData(r2, data)
    print("Positive case completed.")
    """
    NEGATIVE CASE
    -------------
    Reasoning for the negative case:
    --------------------------------
    Compute the path using Dijkstra algorithm and then update FIB of routers along the path where the destination router is r2.
    So to perform negative testing, select any router apart from destination router r2 for sending a packet from r1.
    Starting from r1, the destination field of r1 FIB will not contain any router apart from destination router r2, that is the condition {if dest in self.lib} evaluates to False.
    Hence the packet will be dropped.
    
    Basically pick a node not along the path from r1 to reach r2. Or specify a router that is not present in the topology.
    """
    logger.info("NEGATIVE CASE:")
    logger.info("--------------")
    data = "-->[Test data from {} to {}]".format(r1, r3)
    net.get_router_by_name(r1).sendData(r3, data)
    print("Negative case completed.")
    logger.info("-"*100)
