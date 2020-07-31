from kamene.all import *
import sys



def tcp_stream(infile):
    pcaps = rdpcap(infile)
    tcps = []
    udps = []
    for packet in pcaps:
        try:
            connect_type = packet[IP].proto
            
            if connect_type == 6:   #tcp
                seq_nunber = packet[IP][TCP].seq
                tcps.append(packet)
            elif connect_type == 17:    #udp
                udps.append(packet)
            
        except:
            pass
            
    
    tcps = sorted(tcps, key = lambda x: x[IP][TCP].seq)
    return tcps, udps    
                
if __name__ == "__main__":
    infile = sys.argv[1]
    tcps, udps = tcp_stream(infile)
    print('tcp:', len(tcps), 'udp:',len(udps))
