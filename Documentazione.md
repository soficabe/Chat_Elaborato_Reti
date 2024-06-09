# Sistema di Chat Client-Server
## Sofia Caberletti 0001071418
## Introduzione
Il progetto consiste nella realizzazione di un semplice sistema di chat client-server in linguaggio Python. Questo programma permette a più client di comunicare tra di loro tramite la connessione ad uno stesso server che gestisce i messaggi inviati dai client sulla chat condivisa e comune a tutti i client. Il progetto è basato sul protocollo di rete TCP, che ci garantisce una connessione persistente e affidabile, e utilizza il socket programming e la programmazione concorrente attraverso thread. I thread sono una parte fondamentale di questo progetto in quanto permettono al server di gestire contemporaneamente tutte le connessioni con i vari client assegnando ad ognuna di queste connessioni un thread e allo stesso tempo permette di mantenere attivo il processso  di accettazione di ulteriori client con un ulteriore thread a parte. Il progetto utilizza anche la libreria grafica Tkinter per creare la GUI della chat.

## Server

## Client

## Funzionamento ed Esecuzione
Poichè il server e il client possano comunicare ci sarà bisogno di utilizzare una rete LAN o una connessione localhost.
Per prima cosa si dovrà avviare il server eseguendo il relativo codice e successivamente si potrà eseguire il codice del client più volte per un massimo di 5 istanze di client. Una volta collegati al server i vari client si potranno unire alla chat dove ogni messaggio che manderanno sarà visualizzato in broadcast da tutti gli altri client connessi.
