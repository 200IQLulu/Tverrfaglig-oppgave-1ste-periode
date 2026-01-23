import sys
import site
import os

site.addsitedir('/var/www/Tverrfaglig-oppgave-1ste-periode/env/lib/python3.13/site-packages')

sys.path.insert(0, '/var/www/Tverrfaglig-oppgave-1ste-periode')

os.chdir('/var/www/Tverrfaglig-oppgave-1ste-periode')

os.environ['VIRTUAL_ENV'] = '/var/www/Tverrfaglig-oppgave-1ste-periode/env'
os.environ['PATH'] = '/var/www/Tverrfaglig-oppgave-1ste-periode/env/bin:' + os.environ['PATH']

from app import app as application
