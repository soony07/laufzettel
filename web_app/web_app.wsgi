import sys
sys.path.insert(0,"xxxxxxxxx/wsgi/laufzettel")

from web_app import create_app
application = create_app()
