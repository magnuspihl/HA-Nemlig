from . import webapi


def search_products(query='', take=10):
    return webapi.get('/s/0/1/0/Search/Search', params={
        'query': query,
        'take': take,
    })

def get_product_by_url(url):
    resp = webapi.getRoot('/' + url, params={
        'GetAsJson': '1'
    })
    if (len(resp['content']) == 0):
        return None
    product = resp['content'][0]
    return {
        'Id': product['Id'],
        'Url': product['Url'],
        'Name': product['Name'],
        'Text': product['Text'],
        'Image': product['Media'][0]['Url'],
        'EnergyKcal': product['Declarations']['EnergyKcal'],
        'InStock': product['Availability']['IsAvailableInStock'],
        'Price': product['Price'],
        'SaleBeforeLastSalesDate': product['SaleBeforeLastSalesDate'],
        'Group': product['ProductMainGroupName'],
        'Category': product['ProductCategoryGroupName']
    }


def get_product(id):
    search = search_products(id, 1)
    if (search['ProductsNumFound'] == 0):
        return None
    product = search['Products']['Products'][0]
    url = product['Url']
    return get_product_by_url(url)