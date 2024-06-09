#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#dizionario che associa i vari socket ai rispettivi nickname dei client
clients = {}
#dizionario che associa i vari socket ai rispettivi indirizzi dei client
addresses= {}

hostIP = ''
hostPort = 53000
bufferSize = 1024
hostAddress = (hostIP, hostPort)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(hostAddress)

""" Accetta le connessioni dei client in entrata."""
def accept_connections():
    while True:
        try:
            #Attendo la richiesta di connessione
            clientSocket, clientAddress = serverSocket.accept()
            print("%s:%s si è collegato." % clientAddress)
            clientSocket.send(bytes("Ciao! Digita il tuo nickname.", "utf8"))
            #Aggiunta dell'indirizzo utente alla lista degli indirizzi
            addresses[clientSocket] = clientAddress
            #Creazione ed avvio del thread di gestione del client
            #(un solo thread per ogni client)
            Thread(target=manage_client, args=(clientSocket,)).start()
        except OSError as e:
            print("Errore nell'accettazione delle connessioni in entrata: ", e)
            break
        
"""Gestisce la connessione di un singolo client."""
def manage_client(clientSocket):
    try:
        #Impostazione del nickname e invio del messaggio di benvenuto
        name = clientSocket.recv(bufferSize).decode("utf8")
        wellcomeMsg = 'Ciao %s! Per lasciare la chat scrivi {quit}.' % name
        clientSocket.send(bytes(wellcomeMsg, "utf8"))
        #Notifico tutti i client che un nuovo client si è unito alla chat
        msg = "%s si è unito all chat!" % name
        broadcast_message(bytes(msg, "utf8"))
        #Aggiunta del nickname alla lista dei client
        clients[clientSocket] = name
        #Gestione da parte del server della chat del client
        while True:
            #Mi metto in ascolto dei messaggi in entrata
            #Se il messaggio è diverso dal messaggio di interruzzione della chat
            #lo invio a tutti gli altri client in broadcast se no interrompo
            #la connessione del client
            msg = clientSocket.recv(bufferSize)
            if msg != bytes("{quit}", "utf8"):
                broadcast_message(msg, name+": ")
            else:
                clientSocket.send(bytes("{quit}", "utf8"))
                clientSocket.close()
                del clients[clientSocket]
                address = addresses[clientSocket]
                del addresses[clientSocket]
                print("%s:%s si è scollegato." % address)
                broadcast_message(bytes("%s ha abbandonato la Chat." % name, "utf8"))
                break
    except OSError as e:
        print("Errore nella gestione del client: ", e)
        if clientSocket in clients:
            name = clients[clientSocket]
            del clients[clientSocket]
        if clientSocket in addresses:
            address = addresses[clientSocket]
            del addresses[clientSocket]
            clientSocket.close()
        print("%s:%s si è scollegato." % address)
        broadcast_message(bytes("%s ha abbandonato la Chat." % name, "utf8"))
            
""" Invia un messaggio in broadcast, cioè li invia a tutti i client connessi."""
def broadcast_message(msg, prefix=""):
    for clientSocket in clients:
        try:
            clientSocket.send(bytes(prefix, "utf8")+msg)
        except OSError as e:
            print("Errore nell'invio del messaggio a ", clients[clientSocket], ": ", e)
            clientSocket.close()
            del clients[clientSocket]
            del addresses[clientSocket]


if __name__ == "__main__":
    try: 
        serverSocket.listen(5)
        print("Waiting for a connection ...")
        #thread principale di ascolto dei client che vogliono collegarsi al server
        acceptThread = Thread(target=accept_connections)
        acceptThread.start()
        acceptThread.join()
    except KeyboardInterrupt:
        print("Closing the server ...")
    finally:
        serverSocket.close()