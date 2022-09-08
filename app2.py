from urllib import response
from flask import Flask, render_template, request, jsonify

from chat import get_response
 
app2 = Flask(__name__)

@app2.route("/")
def index_get():
    return render_template("map.html")

if __name__ == "__main__":
    app2.run(debug=True)