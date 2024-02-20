import os, logging
#from synthesizeExtra import textToSpeech
from synthesizeLong import synthesize_long_audio
from flask_cors import CORS

from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable CORS so that requests from different origins aren't block
cors = CORS(app)


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    logger.debug("Hello World")
    logger.debug(__name__)
    return f"Hello {name}!"


@app.route("/readoutloud", methods=["POST"])
def readOutLoud():
    logger.debug("POST REQUEST /readOutLoud")
    data = request.get_json()
    articleContent = data.get('articleContent') or data[articleContent]
    if articleContent is None:
        logger.debug("No articleContent found")
        return {"error": "No articleContent found"}
    

    logger.debug("Starting") 
    filename =  synthesize_long_audio(articleContent)
    logger.debug(filename)
    res = jsonify({"filename": filename})
    res.headers.set('Access-Control-Allow-Origin', '*')
    res.headers.set('Access-Control-Allow-Methods', '*')
    res.headers.set('Access-Control-Allow-Headers', '*')

    return res
    # else:
    #     raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))