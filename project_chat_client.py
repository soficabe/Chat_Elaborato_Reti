#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

hostIP = input('Inserire IP del Server host: ')
hostPort = input('Inserire porta del server host: ')
if not hostPort:
    hostPort = 53000
else:
    hostPort = int(hostPort)

bufferSize = 1024
hostAddress = (hostIP, hostPort)

"""Gestisce la ricezione dei messaggi dal server."""
def receive_message():
    while True:
        try:
            #ci mettiamo in ascolto dei messaggi che arrivano dal server sul socket del client
            msg = clientSocket.recv(bufferSize).decode("utf8")
            if msg != "{quit}":
                msgList.insert(tkt.END, msg)
            else:
                clientSocket.close()
            #Se viene rilevato un errore probabilmente il client ha abbandonato la chat
        except OSError as e:
            print("Errore nella ricezione del messaggio: ", e)
            break
        
"""Gestisce l'invio dei messaggi al server."""
def send_message(event=None):
    try:
        msg = msgToSend.get()
        msgToSend.set("")
        #invio del messaggio sul socket
        clientSocket.send(bytes(msg, "utf8"))
        #se il messaggio corrisponde al messaggio di uscita dalla chat
        #interrompo la connessione
        if msg == "{quit}":
            clientSocket.close()
            window.destroy()
    except OSError as e:
        print("Errore nell'invio del messaggio: ", e)
        
"""Invocata alla chiusura della finestra grafica della chat."""
def on_closing(event=None):
    msgToSend.set("{quit}")
    send_message()

"""Creo la Gui Tkinter della chat del client"""
#Creazione della finestra principale
window = tkt.Tk()
window.title("Chat Interface")
window.configure(bg="dark khaki")
window.geometry("400x380")

#Creazione del campo e della variabile stringa per contenere i messaggi da inviare
msgFrame = tkt.Frame(window)
msgToSend = tkt.StringVar()
msgToSend.set("Digita qui!")
scrollbar = tkt.Scrollbar(msgFrame)

#Creazione dello spazio in cui vengono mostrati i messaggi inviati
msgList = tkt.Listbox(msgFrame, height=20, width=60, yscrollcommand=scrollbar.set, bg="lemon chiffon")
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msgList.pack(side=tkt.LEFT, fill=tkt.BOTH)
msgList.pack()
msgFrame.pack()

#Creazione del campo di input associato alla variabile stringa
entryField = tkt.Entry(window, textvariable=msgToSend)
#Associazione della funzione send_message al tasto Return e al bottono INVIO
entryField.bind("<Return>", send_message)
entryField.pack()
sendButton = tkt.Button(window, text="INVIO", command=send_message)
sendButton.pack()

#Chiusura tramite la X della finestra grafica
window.protocol("WM_DELETE_WINDOW", on_closing)


"""Connessione del client al server."""
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(hostAddress)
    
    #thread di ricezione dei messaggi mandati al client dal server 
    #(un solo thread per ogni client)
    receiveThread = Thread(target=receive_message)
    receiveThread.start()
    #Avvio della Gui
    tkt.mainloop()
except OSError as e:
    print("Errore durante la connessione al server: ", e)
    clientSocket.close()