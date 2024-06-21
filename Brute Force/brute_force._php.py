import requests
from bs4 import BeautifulSoup

def extract_value(url, session):
    
    dizionario = {
        'token':'',
        'phpmyadmin':''
    }

    # Effettua una richiesta GET alla pagina web utilizzando la sessione
    response = session.get(url)

    # Verifica che la richiesta sia andata a buon fine (status code 200)
    if response.status_code == 200:
        # Analizza il contenuto HTML della risposta utilizzando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trova il tag <input> con name='token' e estrai il suo valore 'value'
        token_tag = soup.find('input', {'name': 'token'})
        if token_tag:
            dizionario['token'] = token_tag.get('value')
        else:
            print("Token non trovato nella pagina.")
            return None
    else:
        print(f"Errore nella richiesta GET: {response.status_code} - {response.reason}")
        return None
    
    phpmyadmin_tag = soup.find('input', {'name': 'phpMyAdmin'})

    if phpmyadmin_tag:
        dizionario['phpmyadmin'] = phpmyadmin_tag.get('value')
    else:
        print("phpmyadmin non trovato nella pagina.")
        return None
    
    return dizionario       

url = 'http://192.168.50.101/phpMyAdmin/'  # Sostituisci con l'URL reale della pagina web
session = requests.Session()
dizio = extract_value(url, session)
    
if dizio['token']:
    print(f"Token estratto: {dizio['token']}")
else:
    print("Impossibile estrarre il token.")

if dizio['phpmyadmin']:
    print(f"phpMyAdmin estratto: {dizio['phpmyadmin']}")
else:
    print("Impossibile estrarre il token.")
new_url = f'http://192.168.50.101/phpMyAdmin/index.php?token={dizio['token']}&phpMyAdmin={dizio['phpmyadmin']}'
dati = { 
        'pma_username': 'ro',
        'pma_password': '',
    }

response = session.post(new_url, dati)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)
if response.text.find('Access denied') != -1:
    print("User trovato!")
