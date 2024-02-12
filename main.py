import os
from synthesizeExtra import textToSpeech

from flask import Flask,send_file, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

@app.route("/readoutloud", methods=["POST"])
def readOutLoud():
    url = request.form.get('url')
    if url is None:
        return "No url found"
    
    filename =  textToSpeech(url)

    return send_file(filename, mimetype="audio/mp3")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))