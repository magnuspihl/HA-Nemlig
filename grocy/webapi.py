import time
import requests

API_ROOT = 'https://mariemagnus.duckdns.org:9192/api'
API_KEY = 'jF9mlqf6A47JYFfFyYmO9uwpYlO30gKBJYMN31lrix55NQCsEF'

__session = requests.Session()

class GrocyException(Exception):
    pass

def get(path, **kwargs):
    return __send('GET', API_ROOT, path, **kwargs)
def test_get(path, **kwargs):
    return __test('GET', API_ROOT, path, **kwargs)

def post(path, **kwargs):
    return __send('POST', API_ROOT, path, **kwargs)
def test_post(path, **kwargs):
    return __test('POST', API_ROOT, path, **kwargs)

def put(path, **kwargs):
    return __send('PUT', API_ROOT, path, **kwargs)
def test_put(path, **kwargs):
    return __test('PUT', API_ROOT, path, **kwargs)

def delete(path, **kwargs):
    return __send('DELETE', API_ROOT, path, **kwargs)
def test_delete(path, **kwargs):
    return __test('DELETE', API_ROOT, path, **kwargs)


def __send(method, root, path, **kwargs):
    time.sleep(1)  # poor mans rate limiting
    headers = {'GROCY-API-KEY': API_KEY}
    if ('headers' in kwargs):
        headers.update(kwargs.get('headers'))
    kwargs.pop('headers', None)
    response = __session.request(method, root + path, headers=headers, **kwargs)
    
    if response.status_code == 400:
        message = response.json()['ErrorMessage']
        raise GrocyException(message)
    try:
        response.raise_for_status()
    except:
        print(response.text)
        raise
    return response.json()


def __test(method, root, path, **kwargs):
    time.sleep(1)
    headers = {'GROCY-API-KEY': API_KEY}
    if ('headers' in kwargs):
        headers.update(kwargs.get('headers'))
    kwargs.pop('headers', None)
    response = __session.request(method, root + path, headers=headers, **kwargs)
    return response.status_code