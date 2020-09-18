import nemlig as nemlig
import grocy as grocy

def grocy_shopping_list_to_nemlig_basket():
    return None

def nemlig_order_to_grocy(orderNumber, addToStock):
    nemlig.login("magnus.pihl@gmail.com", "barbadini1")
    try:
        order = nemlig.get_order_with_products(orderNumber)
    except:
        print('Failed to get order: ' + orderNumber)
    for line in order['lines']:
        product = line['product']
        try:
            grocy.create_or_update_product(product['Id'], product['Url'], product['Name'], product['Text'], product['Image'], product['EnergyKcal'], True, True, 1, product['SaleBeforeLastSalesDate'], 5)
        except:
            print('Failed to create/update product: '+ product['Url'])
        if addToStock == True:
            grocy.stock_add(product['Id'], line['amount'], line['price'], product['SaleBeforeLastSalesDate'])

def nemlig_order_numbers(skip, take):
    nemlig.login("magnus.pihl@gmail.com", "barbadini1")
    orders = nemlig.get_order_history(skip, take)
    orderNumbers = []
    for order in orders['Orders']:
        orderNumbers.append(order['Id'])
    return orderNumbers

#grocy.create_or_update_product('5030115', 'appelsinjuice-oeko-5030115', 'Appelsinjuice øko.', '', 'https://live.nemligstatic.com/scommerce/images/appelsinjuice-oeko.jpg?i=vxdEUDoo/5030115', 40, True, True, 1, 30, 5)

for orderNumber in nemlig_order_numbers(0, 1000000):
    orderNumber = str(orderNumber)
    nemlig_order_to_grocy(orderNumber, False)
    print('Processed order ' + orderNumber)

#nemlig_order_to_grocy(56963369, False)