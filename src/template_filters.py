from src import app
from datetime import datetime


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")