from . import webapi

def get_favorites():
    favs = webapi.getRoot('/favoritter?GetAsJson=1&t=2020012214-60-900&d=2')
    settings = favs['Settings']
    for x in favs['content']:
        if 'ProductGroupId' in x:
            url = '/{0}/{1}/{2}/{3}/Products/GetByProductGroupId?pageindex=-1&pagesize=-1&productGroupId={4}'.format(settings['CombinedProductsAndSitecoreTimestamp'], settings['TimeslotUtc'], settings['DeliveryZoneId'], settings['UserId'], x['ProductGroupId'])
            print(url)
            
            group = webapi.get(url)
            for p in group['Products']:
                print(p['Name'])