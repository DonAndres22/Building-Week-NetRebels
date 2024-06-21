import requests as rq
import validators as vl
from requests.exceptions import RequestException, ConnectionError, Timeout

def check_http_methods(url):
    allMethods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'CONNECT', 'PROPFIND', 'REPORT', 'MKCOL', 'LOCK', 'UNLOCK', 'COPY', 'MOVE', 'PURGE']
    enabledMethods = []
    unauthorizedMethods = []
    forbiddenMethods = []
    notfoundMethods = []
    otherMethods = []

    for method in allMethods:
        try:
            response = rq.request(method, url, timeout=5)
            if response.status_code == 200:
                enabledMethods.append(method)
            elif response.status_code == 401:
                unauthorizedMethods.append(method)
            elif response.status_code == 403:
                forbiddenMethods.append(method)
            elif response.status_code == 404:
                notfoundMethods.append(method)
            else:
                otherMethods.append((method, response.status_code))
        except ConnectionError:
            print(f"Connection error with method {method}: Unable to establish a connection.")
        except Timeout:
            print(f"Timeout error with method {method}: The request timed out.")
        except RequestException as e:
            print(f"Error with method {method}: {e}")

    return enabledMethods, unauthorizedMethods, forbiddenMethods, notfoundMethods, otherMethods

def main():
    path = input("Enter the path (URL) to check: ")
    if not path.startswith("http"):
        path = "http://" + path
    if not vl.url(path):
        print("Invalid URL. Please enter a valid URL.")
        return

    enabledMethods, unauthorizedMethods, forbiddenMethods, notfoundMethods, otherMethods = check_http_methods(path)

    if enabledMethods:
        print(f"Enabled HTTP methods for {path}: {', '.join(enabledMethods)}")
    if unauthorizedMethods:
        print(f"Unauthorized HTTP methods for {path}: {', '.join(unauthorizedMethods)}")
    if forbiddenMethods:
        print(f"Forbidden HTTP methods for {path}: {', '.join(forbiddenMethods)}")
    if notfoundMethods:
        print(f"404 not found HTTP methods for {path}: {', '.join(notfoundMethods)}")
    if otherMethods:
        other_methods_str = ', '.join([f"{method} ({status})" for method, status in otherMethods])
        print(f"Other non valid HTTP methods for {path}: {other_methods_str}")

main()
