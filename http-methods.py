import requests as rq
import validators as vl

def check_http_methods(url):
    commonMethods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'PATCH', 'CONNECT', 'PROPFIND', 'REPORT', 'MKCOL', 'LOCK', 'UNLOCK', 'COPY', 'MOVE', 'PURGE']
    enabledMethods = []

    for method in commonMethods:
        try:
            response = rq.request(method, url, timeout = 5)
            if response.status_code != 405:  # 405 Method Not Allowed
                enabledMethods.append(method)
        except rq.exceptions.RequestException as e:
            print(f"Error with method {method}: {e}")

    return enabledMethods

def main():
    path = input("Enter the path (URL) to check: ")
    if not vl.url(path):
        print("Invalid URL. Please enter a valid URL.")
    if not path.startswith("http"):
        path = "http://" + path

    enabledMethods = check_http_methods(path)
    print(f"Enabled HTTP commonMethods for {path}: {', '.join(enabledMethods)}")

main()