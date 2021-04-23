"""
OII vis
pixel-tree, 2020.
"""

import os

from flask import Flask, send_file

app = Flask(__name__,
            static_url_path="",
            static_folder=os.path.abspath("./static"))


# General.
@app.route('/', methods=['GET', 'POST'])
def index():
    return send_file("./static/index.html")


# wsgi.py for deployment; this as main for dev.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
