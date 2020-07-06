from django.shortcuts import render
from bbrest import BbRest
from config import adict

KEY = adict['learn_rest_key']
SECRET = adict['learn_rest_secret']
LEARNFQDN = adict['learn_rest_fqdn']
# Create your views here.

def index(request):
    """View function for home page of site."""
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetVersion()
    version_json = resp.json()

    context = {
        'learn_server': LEARNFQDN,
        'version_json' : version_json,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def whoami(request):
    """View function for whoami page of site."""
    bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
    resp = bb.GetUser("userName:mkauffman")
    user_json = resp.json()
    context = {
        'user_json': user_json,
    }
    print('views.py index(request) calling render...')
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'whoami.html', context=context)