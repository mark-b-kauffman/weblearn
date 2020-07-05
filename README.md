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

* **learn_rest_fqdn** should be set to your learn instances domain. Be sure to avoid the request scheme, i.e. `mylearn.blackboard.edu`


## To Run

First run `pip install -r requirements.txt`  and then `python manage.py runserver`