from flask.ext.script import Manager
from veronica import app

application = app

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug=True)

