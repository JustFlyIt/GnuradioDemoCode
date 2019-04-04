"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import socket
import sys
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC   SAVE TEMPORARILY"""
        gr.sync_block.__init__(
            self,
            name='SendDataToRH_Block  ',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param

    def work(self, input_items, output_items):
	# First Task: Do the passthrough work first
        output_items[0][:] = input_items[0] * self.example_param

	# Second Task: Transmit data over socket to Redhawk
	dataPacket = makeStringPacket(input_items[0])

        sendDataPacket(dataPacket)

        return len(output_items[0])


def sendDataPacket(dataPacket):
    #open socket if not done
    HOST = '127.0.0.1'
    PORT = 9999
    freq = 500.0

    # Transmit and close socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(dataPacket)
    sock.close()

printPacket = 0
	
"""
Makes the string packet of [Sample Period, [Samples]]
such that: "p,s1,s2,s3,...,sN"
Each value should be convertible to float or int.
"""
def makeStringPacket(samples):
    global printPacket

    freq = 11000
    periodSample = 1.0/(freq*8.0)

    fPacket = [periodSample] + samples
    strPacket = ""
    for f in fPacket:
	strPacket += str("%f," % f)
    strPacket = strPacket[:-1]
    if (printPacket==1):    
	print strPacket
        printPacket = 0
    return strPacket
