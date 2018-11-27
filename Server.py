# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 21:00:30 2018

@author: ignap
"""


import socket
import sys
from threading import Thread

def Conexion(connection,client_address):
    global libreria
    global hostOnline
    try:
        print >>sys.stderr, 'connection from', client_address
        while True:
            data = connection.recv(16)
            if data == "h4x0r":
                connection.send("Conectado")
                if data:
                    lista = []
                    lista.append(client_address)
                    while True:
                        files = connection.recv(1024)
                        if files != "fin":
                            print ":",files 
                            lista.append(files)
                            connection.send("ok")
                            #envia el "ok" de que recibió el nombre del archivo
                        else:
                            connection.send("Lista Recibida")
                            found = False
                            for i in libreria:
                                if i[0][0] == client_address[0]:
                                    i = lista
                                    found = True
                                    break
                            if found == False:
                                libreria.append(lista)
                            print libreria
                            hostOnline.append(client_address)
                            break
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
                
         
                
                for i in libreria:
                    if i[0][0] == client_address[0]:
                        continue
                    else:
                        j=1
                        while j < len(i):
                            connection.send(i[j])
                            print >> sys.stderr, 'sending item ', j , 'to ', client_address
                            print connection.recv(4)
                            j = j+1
                connection.send("fin")
 
                data = connection.recv(1024)
                print data 
                encontrado = False
                while data != "Close":
                    print data
                    IP = ""
                    for i in libreria:
                        for j in i:
                            if i.index(j) == 0:
                                IP = j[0]
                            else: 
                                if j == data:
                                    encontrado = True
                                    print IP
                                    connection.send(IP)
                                    print "encontrado"
                                    
                    if encontrado == False:
                        connection.send("100")
                    data = connection.recv(1024)
                for i in libreria:
                    if i[0][0] == client_address:
                        libreria.remove(i)
                connection.send("Exit")
                connection.close()
                break
                
                
                
                
            
            else:
                connection.send("Denegado")
                if data:
                    print >>sys.stderr, 'sending data back to the client: Denegado'
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
    except socket.error, msg:
        print msg
        for i in libreria:
            if i[0][0] == client_address[0]:
                libreria.remove(i)
        connection.close()
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.50.24', 7777)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)
libreria = []
hostOnline = []
while True:
    print "entrando al while"
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    t = Thread(target=Conexion, args=(connection,client_address))
    t.start()