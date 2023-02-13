from django.shortcuts import render
import xmlrpc.client
from odooconfig import models

def realtor(request):
    models.calculateBestOffer() 
    context = {
                'flats':models.getFlatTable(),
                'products':models.getProductTable(),
                'stock':models.getQtyFlat(),
              }
    return render(request, 'odoorealtor/flat.html',context)

def offer(request):
    
    login=request.POST['login']

    offer = request.POST['offer']

    flat_id = int(request.POST['flat'])
    
    result = ""
  
    
    if(models.isBuyer(login)):
        result="Hi "
        result+=login
    else:
        id = models.createBuyer(login)
        result=login
        result+=" You have been registered"
    
    idBuyer=models.getIdBuyer(login)
    try:
        models.createOffer(flat_id,idBuyer,offer)
        models.calculateBestOffer()          
        result+=". Updated offer!"
    except:
        result+=". Invalid offer, make sure your offer is greater than or equal 90 percent of the price"
    
    

    context = {
                'result':result,
                
              }
    return render(request, 'odoorealtor/resultoffer.html',context)