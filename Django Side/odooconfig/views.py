from django.shortcuts import render
import xmlrpc.client
from . import models
myFlats=""

def index(request):

    return render(request, 'odooconfig/odooConnection.html')

def connection(request):

    username=request.POST['username']

    password = request.POST['password']

    database=request.POST['database']

    url =request.POST['yoururl']

    
    result = ""
    try:
        connexion=models.connect(username,password, database,url)
        if connexion:
            
            result = "Passed"
        else:
            result = "Failed"
    except:
             result = "Failed"

    context = {
                'result':result,
                
              }
    return render(request, 'odooconfig/resultConnection.html',context)

