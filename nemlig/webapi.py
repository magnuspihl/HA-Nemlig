import time
import requests

WEB_ROOT = 'https://www.nemlig.com'
API_ROOT = 'https://www.nemlig.com/webapi'

__session = requests.Session()


class NemligException(Exception):
    pass

def getRoot(path, **kwargs):
    return __send('GET', WEB_ROOT, path, **kwargs)


def get(path, **kwargs):
    return __send('GET', API_ROOT, path, **kwargs)


def post(path, **kwargs):
    return __send('POST', API_ROOT, path, **kwargs)


def __send(method, root, path, **kwargs):
    time.sleep(1)  # poor mans rate limiting
    if 'XSRF-COOKIE-TOKEN' in __session.cookies:
        #print({"x-xsrf-token": __session.cookies['XSRF-COOKIE-TOKEN'], "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin"})
        response = __session.request(method, root + path, headers={"x-xsrf-token": __session.cookies['XSRF-COOKIE-TOKEN'], "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin"}, **kwargs)
    else:
        response = __session.request(method, root + path, **kwargs)
    if response.status_code == 400:
        message = response.json()['ErrorMessage']
        raise NemligException(message + ' (' + response.url + ')')
    try:
        response.raise_for_status()
    except:
        print(response.text)
        raise
    return response.json()
