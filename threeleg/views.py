from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from bbrest import BbRest
from config import adict
import jsonpickle
import uuid

KEY = adict['learn_rest_key']
SECRET = adict['learn_rest_secret']
LEARNFQDN = adict['learn_rest_fqdn']
# Create your views here.

def threeindex(request):
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
    return render(request, 'threeindex.html', context=context)

def whoami(request):
    """View function for whoami page of site."""
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'whoami' # So after we have the access token we know to come back here.
        # The following does maintain the https: scheme if that was used with the incomming request.
        # BUT because I'm terminating the tls at the ngrok server, my incomming request is http.
        # Hence the redirect to get_auth_code is http in development. But we want our redirect_uri to be
        # have a scheme of https so that the Learn server can redirect back through ngrok with our 
        # secure SSL cert. We'll have to build a redirect_uri with the https scheme in the 
        # get_auth_code function.
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    resp = bb.call('GetUser', userId = "me", sync=True ) #Need BbRest to support "me"
    user_json = resp.json()
    context = {
        'user_json': user_json,
        'access_token': bb.token_info['access_token']
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'whoami.html', context=context)

def courses(request):
    """View function for courses page of site."""
    bb_json = request.session.get('bb_json')
    if (bb_json is None):
        bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}" )
        bb_json = jsonpickle.encode(bb)
        print('pickled BbRest putting it on session')
        request.session['bb_json'] = bb_json
        request.session['target_view'] = 'courses'
        return HttpResponseRedirect(reverse('get_auth_code'))
    else:
        print('got BbRest from session')
        bb = jsonpickle.decode(bb_json)
        if bb.is_expired():
            print('expired token')
            request.session['bb_json'] = None
            whoami(request)
        bb.supported_functions() # This and the following are required after
        bb.method_generator()    # unpickling the pickled object.
        print(f'expiration: {bb.expiration()}')

    resp = bb.call('GetCourses', sync=True ) 
    courses_json = resp.json()
    context = {
        'courses_json': courses_json,
        'access_token': bb.token_info['access_token']
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'courses.html', context=context)

def get_auth_code(request):
    # Happens when the user hits whoami the first time and hasn't authenticated on Learn
    # Part I. Request an authroization code oauth2/authorizationcode
    print(f"In get_auth_code: REQUEST URI:{request.build_absolute_uri()}")
    bb_json = request.session.get('bb_json')
    print('got BbRest from session')
    bb = jsonpickle.decode(bb_json)
    bb.supported_functions() # This and the following are required after
    bb.method_generator()    # unpickling the pickled object. 
    # The following gives the path to the resource on the server where we are running, 
    # but not the protocol or host FQDN. We need to prepend those to get an absolute redirect uri.
    redirect_uri = reverse(get_access_token)
    absolute_redirect_uri = f"https://{request.get_host()}{redirect_uri}"
    # absolute_redirect_uri = request.build_absolute_uri(redirect_uri)
    state = str(uuid.uuid4())
    request.session['state'] = state
    authcodeurl = bb.get_auth_url(redirect_uri=absolute_redirect_uri, state=state)
    print(f"AUTHCODEURL:{authcodeurl}")
    return HttpResponseRedirect(authcodeurl)

def get_access_token(request):
    # Happens when the user hits whoami the first time and hasn't authenticated on Learn
    # Part II. Get an access token for the user that logged in. Put that on their session.
    bb_json = request.session.get('bb_json')
    target_view = request.session.get('target_view')
    print('got BbRest from session')
    bb = jsonpickle.decode(bb_json)
    bb.supported_functions() # This and the following are required after
    bb.method_generator()    # unpickling the pickled object.
    # Next, get the code parameter value from the request
    redirect_uri = reverse(get_access_token)
    absolute_redirect_uri = f"https://{request.get_host()}{redirect_uri}"
    state = request.GET.get('state', default= "NOSTATE")
    print(f'GOT BACK state: {state}')
    stored_state = request.session.get('state')
    print(f'STORED STATE: {stored_state}')
    if (stored_state != state):
        return HttpResponseRedirect(reverse('index'))
    code =  request.GET.get('code', default = None)
    if (code == None):
        return HttpResponseRedirect(reverse('index'))
    #Rebuild a new BbRest object to get an access token with the user's authcode.
    user_bb = BbRest(KEY, SECRET, f"https://{LEARNFQDN}", code=code, redirect_uri=absolute_redirect_uri )
    bb_json = jsonpickle.encode(user_bb)
    print('pickled BbRest putting it on session')
    request.session['bb_json'] = bb_json
    return HttpResponseRedirect(reverse(f'{target_view}'))


