from flask import Flask
import GetWbData

app = Flask(__name__)


@app.route('/<string:WbID>')
def hello_world(WbID):
    return GetWbData.huoqu(WbID)


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
