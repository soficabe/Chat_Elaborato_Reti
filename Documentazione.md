# Sistema di Chat Client-Server
## Sofia Caberletti 0001071418
## Introduzione
Il progetto consiste nella realizzazione di un semplice sistema di chat client-server in linguaggio Python. Questo programma permette a più client di comunicare tra di loro tramite la connessione ad uno stesso server che gestisce i messaggi inviati dai client sulla chat condivisa e comune a tutti i client. Il progetto è basato sul protocollo di rete TCP, che ci garantisce una connessione persistente e affidabile, e utilizza il socket programming e la programmazione concorrente attraverso thread. I thread sono una parte fondamentale di questo progetto in quanto permettono al server di gestire contemporaneamente tutte le connessioni con i vari client assegnando ad ognuna di queste connessioni un thread, mantenendo al contempo attivo il processo di accettazione di ulteriori client con un thread separato. Il progetto utilizza anche la libreria grafica Tkinter per creare la GUI della chat.

## Server
Il server svolge il compito di accettazione delle connessioni in entrata, di gestione di ciascun client con un thread dedicato e di condivisione dei messaggi nella chat.  
Per prima cosa viene creato un socket TCP associato all'indirizzo e alla porta del server e avvia il thread `acceptThread` per gestire le richieste di connessione dei client tramite la funzione `accept_connections`. La funzione `accept_connections` grazie al socket mette il server in ascolto delle connessioni in entrata sulla porta specificata (in questo caso la porta 53000). Per ogni connessione accettata, viene creato un nuovo thread che gestisce il client con la funzione `manage_client`.  
La funzione `manage_client` gestisce la connessione di un singolo client. All'inizio, riceve il nickname del client e gli invia un messaggio di benvenuto. Notifica tutti i client della nuova connessione e aggiunge il client al dizionario clients. La funzione poi ascolta i messaggi inviati dal client e li trasmette a tutti i client connessi tramite la funzione `broadcast_message`. Se il client invia il messaggio `{quit}` oppure vengono rilevate delle eccezioni, la connessione viene chiusa e il client viene rimosso dai dizionari clients e addresses.  
La funzione `broadcast_message` trasmettere i messaggi mandati da un client a tutti gli altri client connessi al server. Se si verifica un errore nell'invio del messaggio a un client, il client viene rimosso dai dizionari clients e addresses e la connessione viene terminata.  
Se viene rilevata un'interruzione da tastiera (KeyboardInterrupt), il socket del server viene chiuso.

## Client
Il client si connette al server e utilizza un'interfaccia grafica per inviare messaggi e ricevere i messaggi in entrata.  
L'interfaccia grafica è implementata utilizzando la libreria Tkinter. La finestra della chat mostra i messaggi ricevuti e include un campo di input per digitare nuovi messaggi e un bottone per inviarli.  
Per connettersi al server il client richiede l'indirizzo IP e la porta del server stesso. Se la porta non viene specificata, viene utilizzata la porta di default 53000.  
Il thread `receiveThread` dedicato allo specifico client gestisce la ricezione dei messaggi dal server tramite la funzione `receive_message` . I messaggi ricevuti vengono visualizzati nella lista dei messaggi `msgList`. Se viene ricevuto il messaggio `{quit}`, la connessione viene chiusa.  
La funzione `send_message` gestisce l'invio al server dei messaggi digitati nell'area di input. I messaggi vengono inviati quando l'utente preme il tasto Return o clicca sul bottone INVIO. Se il messaggio è `{quit}`, la connessione viene terminata e la finestra grafica si chiude.  
La funzione `on_closing` viene invocata quando l'utente chiude la finestra della chat tramite la X. La funzione invierà il messaggio `{quit}` e chiuderà la connessione.

## Funzionamento ed Esecuzione
Poichè il server e il client possano comunicare ci sarà bisogno di utilizzare una rete LAN o una connessione localhost (interfaccia di loopback).
Per prima cosa si dovrà avviare il server eseguendo il relativo codice, e successivamente si potrà eseguire il codice del client più volte per un massimo di 5 istanze di client. Una volta collegati al server, i vari client si potranno unire alla chat, dove ogni messaggio che manderanno sarà visualizzato in broadcast da tutti gli altri client connessi.
