import socket

def list_networks(ipv4_only=False):
    ifc = socket.getaddrinfo(socket.gethostname(), None)
    if ipv4_only:
        return [i[4][0] for i in ifc]
    return [i[4][0] for i in ifc if i[0] == socket.AF_INET]