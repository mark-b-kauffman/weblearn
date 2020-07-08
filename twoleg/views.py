from django.shortcuts import render
from bbrest import BbRest
from config import adict

KEY = adict['learn_rest_key']
SECRET = adict['learn_rest_secret']
LEARNFQDN = adict['learn_rest_fqdn']
# Create your views here.

def index(request):
    """View function for home page of site."""
    request.session.flush()  # REMOVE - Just for testing functionality when there is no session.
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetVersion()
    access_token = bb.get_token()
    version_json = resp.json()

    context = {
        'learn_server': LEARNFQDN,
        'version_json' : version_json,
        'access_token' : access_token,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

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