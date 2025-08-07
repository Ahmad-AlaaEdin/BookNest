from flask import Flask

def create_app():
    app = Flask("BookNest",template_folder='app/templates', static_folder='static')
    

    from .routes import main
    app.register_blueprint(main)

   
    return app