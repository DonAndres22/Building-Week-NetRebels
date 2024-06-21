import requests as rq
import validators as vl
from requests.exceptions import RequestException, ConnectionError, Timeout

def check_http_methods(url):
    allMethods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'CONNECT', 'PROPFIND', 'REPORT', 'MKCOL', 'LOCK', 'UNLOCK', 'COPY', 'MOVE', 'PURGE']
    enabledMethods = []
    otherMethods = []

    for method in allMethods:
        try:
            response = rq.request(method, url, timeout=5)
            if response.status_code == 200:
                enabledMethods.append(method)
            else:
                otherMethods.append((method, response.status_code))
        except ConnectionError:
            print(f"Connection error with method {method}: Unable to establish a connection.")
        except Timeout:
            print(f"Timeout error with method {method}: The request timed out.")
        except RequestException as e:
            print(f"Error with method {method}: {e}")

    return enabledMethods, otherMethods

def main():
    path = input("Enter the path (URL) to check: ")
    if not path.startswith("http"):
        path = "http://" + path
    if not vl.url(path):
        print("Invalid URL. Please enter a valid URL.")
        return

    enabledMethods, otherMethods = check_http_methods(path)

    if enabledMethods:
        print(f"Enabled HTTP methods for {path}: {', '.join(enabledMethods)}")
    if otherMethods:
        other_methods_str = ', '.join([f"{method} ##{status}##" for method, status in otherMethods])
        print(f"Other non valid HTTP methods for {path}: {other_methods_str}")

main()
