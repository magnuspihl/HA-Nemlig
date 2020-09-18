from . import webapi
from .product import search_products, get_product_by_url, get_product
from datetime import datetime

def get_order_history(skip=0, take=10):
    return webapi.get('/order/GetBasicOrderHistory', params={
        'skip': skip,
        'take': take,
    })

def get_order(order_number):
    return webapi.get('/order/GetOrderHistory', params={
        'orderNumber': order_number,
    })

def get_order_with_products(order_number):
    order = get_order(order_number)
    lines = []
    for line in order['Lines']:
        product = get_product(line['ProductNumber'])
        if (product is not None):
            lines.append({
                'amount': line['Quantity'],
                'price': line['AverageItemPrice'],
                'product': product
            })
    return {
        'lines': lines,
        'orderNumber': order_number,
        'deliveryDate': datetime.strptime(order['DeliveryDate'], '%d/%m-%Y')
    }