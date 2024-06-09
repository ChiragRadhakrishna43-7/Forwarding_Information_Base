<h1>Forwarding Information Base</h1>

<p align='justify'> The Dijkstra algorithm is used to compute the shortest path between the two routers in the given network configuration. For each router along the shortest path, the FIB data structure is updated. To test this update, a packet is sent from the origin to the destination of the shortest path. This accounts for the positive case. We also do a negative test by sending another packet from a node to another without fib entries to connect them.</p>
<p align='justify'> A FIB data structure is added to the router class which represents the 'forwarding table'. The data structure is flexible. Any data structure is suitable to represent the FIB. Usually, it is a "table" of 2 or 3 columns.  The first is the name of the destination (in real world, that will be the IP address.  For this class, it is the name of the destination router.)  The second column is the "link" leading to a neighboring, directly connected, router, also known as the "next hop."</p>
<p align='justify'> <i>Example: An entry of ('R35', <router object>, 10) means to deliver a packet to the router "R35", the packet should be forwarded to the router object of the tuple and the final cost to reach there is 10.</i></p>
<b>Implementation</b>
<br/>
<p align='justify'>Initialize each router with a fib table consisting of only its directly linked neighbors. <i>(At this point, the link table and fib look very similar.)</i><br/>
Run Dijkstra computation for two random notes. Add a fib entry into each of the router's FIB table along the path.<br/>
Send a packet from the first node of the obtained shortest path to the last node. This can be achieved by implementing "sendData" and "recvData" methods to the router class.<br/>
<i>"sendData" accepts a destination router name (as string) and a data, presumed to be a string.  
It consults the FIB table to see if the destination router is present.  If so, it first encapsulates the data into a "packet" by prefixing a header that has, minimally, the destination's name.  
After the encapsulation, it calls the "recvData" of the next-hop router object to deliver the packet. If its FIB table does not have such entry, the packet is dropped.</i><br/>
<i>"recvData" accepts a packet from the caller and decapsulates it to understand the final destination. If the data is meant for itself, it is simply accepted. 
Otherwise, it uses its own "sendData" method to handle the packet header for the final destination of this packet.</i></p>
