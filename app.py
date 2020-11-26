from flask import Flask
from config import TestingConfig, ProdConfig
from views.router import router

import os

def create_app(testing=False):

    app = Flask(__name__)

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProdConfig)

    app.register_blueprint(router)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()