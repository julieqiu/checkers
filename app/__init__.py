from flask import Flask
import sys
import logging

app = Flask(__name__)


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


from app import views

