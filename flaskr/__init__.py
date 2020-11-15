import os
from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlie')
    )

    if test_config is None:
        # load the instance config, if it exists, when not test
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure that the instance folder exist.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return(render_template('main.html'))

    @app.route('/read/')
    def read():
        return(render_template('read.html'))

    @app.route('/submit/')
    def submit():
        return(render_template('submit.html'))

    from . import db
    db.init_app(app)


    return app
