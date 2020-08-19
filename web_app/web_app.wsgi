import sys
sys.path.insert(0,"/srv/www/ubdocs.aau.at/wsgi/laufzettel")

from web_app import create_app
application = create_app()
