from django.db import models
import xmlrpc.client

connection_info = {}
app_info = {}
def connect(username,password, database,url):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(database, username, password, {})
    model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    hasRight = model.execute_kw(database, uid, password, 'realtor.flat', 'check_access_rights',['read'], {'raise_exception': False})
        
    if hasRight:
        connection_info['common']=common
        connection_info['uid']=uid
        connection_info['model']=model
        connection_info['password']=password
        connection_info['database']=database
        app_info['flatTable']=model.execute_kw(database, uid, password,'realtor.flat', 'search_read', [[]])
        app_info['buyerTable']=model.execute_kw(database, uid, password,'res.partner', 'search_read', [[]])
        app_info['stockTable']=model.execute_kw(database, uid, password,'stock.inventory.line', 'search_read', [[]])
        app_info['offerTable']=model.execute_kw(database, uid, password,'offer.flat', 'search_read', [[]])
        app_info['productTable']=model.execute_kw(database, uid, password,'product.product', 'search_read', [[]])
        return True
    else:
        return False

def updateFlatTable():
    app_info['flatTable']=connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'],'realtor.flat', 'search_read', [[]])

def updateBuyerTable():
    app_info['buyerTable']=connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'],'res.partner', 'search_read', [[]])

def updateOfferTable():
    app_info['offerTable']=connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'],'offer.flat', 'search_read', [[]])

def getFlatTable():
    return app_info['flatTable']

def getBuyerTable():
    return app_info['buyerTable']

def getQtyFlat():
    stok = {}
    for inventory in getStockTable():
        for product in getProductTable():
            
            if(inventory.get("product_id")[0]==product.get("id")):
                stok[product.get("id")]=inventory.get("product_qty")
            
    return stok

def getStockTable():
       return app_info['stockTable']
   
def getOfferTable():
        return app_info['offerTable']
    
def getProductTable():
       return app_info['productTable']
   
def isBuyer(login):
    for buyer in getBuyerTable():
        if (buyer.get("name")==login):
            return True

    return False

def getIdBuyer(login):
    id=0
    for buyer in getBuyerTable():
        if (buyer.get("name")==login):
            id=buyer.get("id") 

    return id

def createBuyer(name):
    id = connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'], 'res.partner', 'create', [{'name': name}])
    updateBuyerTable()
    
def createOffer(flat,buyer,offer):
    id = connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'], 'offer.flat', 'create', [{'flat': flat,'buyer': buyer,'offer': offer}])
    updateOfferTable()
    
def calculateBestOffer():
   

    for offer in getOfferTable():
        count=0
        for otherOffer in getOfferTable():
            if(otherOffer.get("flat")[1]==offer.get("flat")[1]):
                count+=1
        if (count==1):
            id = otherOffer.get("flat")[0]
            newBuyer = otherOffer.get("buyer")[1]
            newMPrice = otherOffer.get("offer")
            connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'], 'realtor.flat', 'write', [[id],{'bestBuyer': newBuyer,'bestPrice': newMPrice}])
        else:
            for otherOffer in getOfferTable():
                if(otherOffer.get("flat")[1]==offer.get("flat")[1] and otherOffer.get("offer")>offer.get("offer")):
                    id = otherOffer.get("flat")[0]
                    newBuyer = otherOffer.get("buyer")[1]
                    newMPrice = otherOffer.get("offer")
                    connection_info['model'].execute_kw(connection_info['database'], connection_info['uid'], connection_info['password'], 'realtor.flat', 'write', [[id],{'bestBuyer': newBuyer,'bestPrice': newMPrice}])
    updateFlatTable()