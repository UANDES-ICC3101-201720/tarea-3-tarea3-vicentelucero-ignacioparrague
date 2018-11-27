# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 21:13:07 2018

@author: Gamma
"""

import socket
import sys
import os
from threading import Thread

def recibir():
    global sock
    global salir
    while True:
        item = raw_input("waiting orders: ")
        sock.send(item)
        resp = sock.recv(1024)
        print resp
        if resp == "100":
            print "file not found"
        elif resp == "Exit":
            print "Exiting Program"
            salir = True
            break
        elif resp != "100" and resp != "Exit":
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (resp, 8000) 
            sock2.connect(server_address)
            print "connecting with: "+resp
            YN = "maybe"
            while YN != "Y" and YN != "N":
                YN = raw_input("start download?(Y/N): ")
            if YN == "Y":
                print "asd"
                sock2.send("PULL"+" "+item)
                #size = int(sock2.recv(1024))
                archivo = open(contenido+'/'+item, 'wb')
                while True:
                    print "asd2"
                    while True:
                        print "asd3"
                        data = sock2.recv(1024)
                        print data
                        if data == "fin" or data == "" or data == "finfinfin":
                            print "break it dowb 1"
                            break
                        archivo.write(data)
                    print "break down 2"
                    break
                print "todo ok teoricamente"
                archivo.close()
                sock2.close()
                exit(1)
                #if datarecv != size:
                    #print "ERROR something failed"
                
                print "finalizada"
    
    
    
def enviar(hosting,contenido):
    send = hosting.recv(1024)
    print "asas"
    send = send.split(" ")
    item = send[1]
    print send
    if send[0] == "PULL":
        archivo = open(contenido+'/'+item, 'rb')
        #hosting.send(str(os.path.getsize(contenido+item)))
        while True:
            while True:
                data = archivo.read(1024)
                if not data:
                    break
                hosting.send(data)
            print "fin envio"
            hosting.send("fin")
            hosting.send("fin")
            hosting.send("fin")
            break
        archivo.close()
    


contenido = "C:/Users/ignap/Desktop/asd"
salir = False
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('192.168.50.24', 7777) 
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


#Input = raw_input()
#Conectando al servidor
try: 
    
    sock.send("h4x0r")

    data = sock.recv(16)
    print >>sys.stderr, 'received "%s"' % data        
    if data == "Conectado":
        for root, dirs, files in os.walk(contenido):
            for filename in files:
                sock.send(filename)
                respuesta = sock.recv(32)
                print respuesta
        sock.send("fin")
        data = sock.recv(16)
        print >>sys.stderr, 'received "%s"' % data

    else:
        print "Clave invalida"
        raw_input()
        sock.close()
        exit(1)
    
    while True:
        items = sock.recv(1024)
        if items != "fin":
            print items, 'asd'
            sock.send("ok")
        else:
            break
        
    
    get = Thread(target=recibir, args=())
    get.start()
      
    hosting = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('192.168.50.13', 8000)
    hosting.bind(server_address)
    # Listen for incoming connections
    hosting.listen(10)
    while True:
        connection, client_address = hosting.accept()
        push = Thread(target=enviar, args=(connection,contenido))
        push.start()
       
        
except socket.error, msg:
    print "Error 400: No connection with the server"
    sock.close()
    exit(1)
        
