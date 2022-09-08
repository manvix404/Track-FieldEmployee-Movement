from urllib import response
from flask import Flask, render_template, request, jsonify

from chat import get_response
 
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    #  TODO: check if the text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)