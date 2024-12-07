from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../instance/config.py")
    
    with app.app_context():
        from . import routes
        return app