from . import webapi
from datetime import datetime
from datetime import timedelta

def stock_add(productId, amount, price, bestBeforeDays):
    bestBeforeDate = datetime.now() + timedelta(days=bestBeforeDays)

    return webapi.post('/stock/products/' + productId + '/add', json={
        'amount': amount,
        'price': price,
        'best_before_date': bestBeforeDate.strftime('%Y-%m-%d')
    })