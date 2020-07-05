README.txt are notes I take as I create. Less formal than a README.md.

Python Environment
  deactivate
  source ~/.bashrc
  workon
  workon my_devcon_django

Django Setup (Modify to use Python 3.7.x or 3.8.x and Django 3.x)
  https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
  python manage.py createsuperuser
  mkauffman markkauffman2000@gmail.com
  settings.py  
    # replace www.avinyet.com with your registred domain,
    #  a domain for which you have a valid SSL cert.
    ALLOWED_HOSTS = ['localhost', 'www.avinyet.com']

SSL Cert:
 To run with https://www.avinyet.com I configured my DNS & ngrok.
 The following starts ngrok and uses the cert I have for the domain.
 $ ~/ngrok tls -region=us -hostname=www.avinyet.com -key ~/avinet.rsaprivatekey.pem -crt ~/avinet.fullchaincert.pem 8000

VS Code:
  Install Microsoft's Python Extension and Pylance  
  Shift-cmd-P Select Python Interpreter.

Django As We Go
  python manage.py runserver
  python manage.py makemigrations
  python manage.py migrate
  python manage.py shell