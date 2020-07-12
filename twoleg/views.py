from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from bbrest import BbRest
from config import adict

KEY = adict['learn_rest_key']
SECRET = adict['learn_rest_secret']
LEARNFQDN = adict['learn_rest_fqdn']
# Create your views here.

def index(request):
    """View function for home page of site."""
    # request.session.flush()  # If you uncomment you can use Home to clear out the 3LO token in session.
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetVersion()
    access_token = bb.token_info['access_token']
    version_json = resp.json()

    context = {
        'learn_server': LEARNFQDN,
        'version_json' : version_json,
        'access_token' : access_token,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def learnlogout(request):
    request.session.flush()
    return HttpResponseRedirect(f"https://{LEARNFQDN}/webapps/login?action=logout")

def getusers(request):
    """View function for getusers page of site."""
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetUsers()
    user_json = resp.json()
    context = {
        'user_json': user_json,
    }
    print('views.py index(request) calling render...')
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'getusers.html', context=context)