from flask import Flask

app = Flask(__name__)

from src import views
from src import views_admin
