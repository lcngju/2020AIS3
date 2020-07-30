from pcapfile import savefile
import sys
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
import binascii



def get_MACip(infile):
    testcap = open(infile, 'rb')
    capfile = savefile.load_savefile(testcap, verbose=True)
    MACip = dict()
    for idx, packet in enumerate(capfile.packets):
        try:
            eth_frame = ethernet.Ethernet(packet.raw())
            ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))
            MAC = eth_frame.src
            ip_t = ip_packet.src
            MACip[MAC] = ip_t
            
        except:
            pass

    return MACip

if __name__ == '__main__':
	
    infile = sys.argv[1]
    print(get_MACip(infile))
