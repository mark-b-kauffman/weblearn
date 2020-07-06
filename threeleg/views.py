from django.shortcuts import render
from bbrest import BbRest
from config import adict
import jsonpickle

KEY = adict['learn_rest_key']
SECRET = adict['learn_rest_secret']
LEARNFQDN = adict['learn_rest_fqdn']
# Create your views here.

def index(request):
    """View function for home page of site."""

    # The following gets/stores the object to access Learn in the user's session.
    # This is key for 3LO web applications so that when you use the app, your
    # session has your object for accessing 
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
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    resp = bb.GetUser("userName:mkauffman")
    user_json = resp.json()
    context = {
        'user_json': user_json,
        'user_token': bb.get_token()
    }
    print('views.py index(request) calling render...')
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'whoami.html', context=context)