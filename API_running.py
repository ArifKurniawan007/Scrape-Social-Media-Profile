from flask import Flask, jsonify, request, abort, make_response
from ScrapeTwitterID import main_twitter
from ScrapeInstagramID import main_instagram
from ScrapeFacebookID import main_facebook
from flask_cors import CORS

app = Flask(__name__)
# CORS =(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/twitter', methods=['GET'])
def getdata01():
    username = request.args.get('username')
    return jsonify(main_twitter(username))

@app.route('/instagram', methods=['GET'])
def getdata02():
    username = request.args.get('username')
    return jsonify(main_instagram(username))

@app.route('/facebook', methods=['GET'])
def getdata03():
    username = request.args.get('username')
    return jsonify(main_facebook(username))



if __name__ == '__main__':
    app.run(host='localhost', port=7770, debug=True)
