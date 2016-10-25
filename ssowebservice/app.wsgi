import os, sys
sys.path.append('/opt/projects/ssowebservice/ssowebservice')
sys.path.append('/opt/projects/ssowebservice/venv/lib/python2.7/site-packages')
activate_env=os.path.expanduser('/opt/projects/ssowebservice/venv/bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))
from app import app as application
