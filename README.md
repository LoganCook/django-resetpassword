#Reset password app - A Django application

This is a token only password reset application for minimal dependency.

## Server
A server needs to be able to:

0. run Python 3
0. has `virtualenv` installed
0. run a web server supports wsgi application
0. be configured to support HTTPS
0. communicate with eRSA's active directory

## Install the application

As an example, assume it is installed to `/var/lib/django-pwd-reset/package` (this is true for all the examples given in this document), run commands:

```shell
sudo su -
mkdir /var/lib/django-pwd-reset
virtualenv -p python3 /var/lib/django-pwd-reset/webapp_env

cd /var/lib/django-pwd-reset
git clone https://github.com/eResearchSA/django-resetpassword.git package

source /var/lib/django-pwd-reset/webapp_env/bin/activate
pip install -r django-resetpassword/requirements.txt

#Update app/settings.py use `dev_settings.py` or `prod_settings.py` as references.
#`prod_settings.py` assmues HTTPS is the only allowed protocol
```

## Configure WSGI

This example shows the directives of mod_wsgi on an Apache 2.4 with Python 3.4 installed.

```INI
    ServerName amin.idpdev.ersa.edu.au
    ServerAlias amin

    WSGIDaemonProcess amin python-path=/var/lib/django-pwd-reset/package/:/var/lib/django-pwd-reset/webapp_env/lib/python3.4/site-packages
    WSGIProcessGroup amin

    #Password reset application access from amin.idpdev.ersa.edu.au
    WSGIScriptAlias /fe /var/lib/django-pwd-reset/package/wsgi.py process-group=amin

    <Directory "/var/lib/django-pwd-reset/package/app">
      <Files "wsgi.py">
        Require all granted
      </Files>
    </Directory>
```

For the numbers of processes and threads, reference [WSGIDaemonProcess](https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIDaemonProcess)
and experiment them.

The application generates a log file which is defined in `settings.py`. Make sure htppd (apache2) user, e.g. `www-data`, has write permission to the log file.

The default templates for generating email and pages are in `ersaauth/templates`. Make changes to suit requirements.

The access url is: auth/password_reset/ under the `WSGIScriptAlias`: e.g. `fe/auth/password_reset/`
