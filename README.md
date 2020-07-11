# BBDN-Web-Learn

This project is set up to demonstrate making REST API calls from Django

To configure:

## Install Python 3.7.x

See https://docs.python.org/3.7/using/index.html

## Install Django 3.x

See https://docs.djangoproject.com/en/3.0/topics/install/

## config_template.py

Copy `config_template.py` to `config.py` and fill in your information:

```
adict = {
    "learn_rest_fqdn" : "your.learnserver.net",
    "learn_rest_key" : "Your REST API KEY GOES HERE NOT Mine",
    "learn_rest_secret" : "Your REST API SECRET GOES HEREer",
}

```

* **learn_rest_fqdn** should be set to the FQDN of your Blackboard Learn instance. Be sure to avoid the request scheme, i.e. use `mylearn.blackboard.edu`


## To Run

* **The Django webserver** should be made available on the public internet with a valid SSL certificate. For development on his local system, the author uses for ngrok to forward from the domain www.avinyet.com to the localhost:8000 with:
```
~/ngrok tls -region=us -hostname=www.avinyet.com -key ~/avinet.rsaprivatekey.pem -crt ~/avinet.fullchaincert.pem 8000
```
* **After cloning from github** run `pip install -r requirements.txt` . Next run `python manage.py migrate` to apply the migrations. And last, start the server with `python manage.py runserver`
