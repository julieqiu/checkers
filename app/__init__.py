from flask import Flask
import sys
from logging import Formatter

app = Flask(__name__)


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def log_to_stderr(app):
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)




from app import views, models
