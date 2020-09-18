from . import webapi
import base64
import requests

PACK_ID = 3
PIECE_ID = 2

def get_products():
    return webapi.get('/objects/products')

def get_product(id):
    return webapi.get('/objects/products/' + id)

def create_or_update_product(id, barcode, name, description, picture, calories, isPackPurchase, isPackStock, factorPurchaseToStock, bestBeforeDays, location):
    product = {
        "id": id,
        "barcode": barcode,
        "name": name,
        "description": description,
        "calories": calories
    }
    if (webapi.get('/objects/products/' + id) is not None):
        #print("Updating product " + id)
        return webapi.test_put('/objects/products/' + id, json=product)
    else:
        #print("Creating product " + id)
        product['picture_file_name'] = transfer_file(picture) if picture is not None else None
        product['qu_id_purchase'] = PACK_ID if isPackPurchase else PIECE_ID
        product['qu_id_stock'] = PACK_ID if isPackStock else PIECE_ID
        product['qu_factor_purchase_to_stock'] = factorPurchaseToStock
        product['default_best_before_days'] = bestBeforeDays
        product['location_id'] = location
        return webapi.post('/objects/products', json=product)

def encodeFilename(filename):
    encodedBytes = base64.b64encode(filename.encode("utf-8")).decode("utf-8")
    return str(encodedBytes)

def upload_file(filename, data):
    encodedFilename = encodeFilename(filename)
    webapi.test_put('/files/productpictures/' + encodedFilename, data=data, headers={'Content-Type': 'application/octet-stream'})

def transfer_file(url):
    filename = filename_from_url(url)
    encodedFilename = encodeFilename(filename)
    resultUrl = '/files/productpictures/' + encodedFilename

    if webapi.test_get(resultUrl) == 200:
        return filename

    data = download_picture(url)
    upload_file(filename, data)

    return filename

def filename_from_url(url):
    if (url.find('?')):
        url = url.split('?', 1)[0]
    if (url.find('/')):
        url = url.rsplit('/', 1)[1]
    return url

def download_picture(url):
    r = requests.get(url, allow_redirects=True, stream=True)
    #r.raw.decode_content = True
    #filename = filename_from_url(url)
    #open(filename, 'wb').write(r.content)
    return r.content