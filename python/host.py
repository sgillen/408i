import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port
NUM_CLIENTS = 5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_list = []

s.bind((HOST, PORT))
s.listen(1)






for i in range(0,NUM_CLIENTS):
    conn, addr = s.accept()
    data = conn.recv(1024)
    print 'Connected by', addr
    client_list.append((conn,addr))
    if not data:
        print "no data"
        
    conn.sendall(data)


while 1:
    
   conn.close()