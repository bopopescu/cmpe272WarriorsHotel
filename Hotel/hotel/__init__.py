import os

from flask import Flask
from flask_oidc import OpenIDConnect
from okta import UsersClient

# This is a factory method for productive deployment
# Use app specific configuration
# For any app local files, use /instnce Folder
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'hotel.sqlite'),
        OIDC_CLIENT_SECRETS=os.path.join(app.instance_path, 'client_secrets.json'),
        OIDC_COOKIE_SECURE=False,
        OIDC_CALLBACK_ROUTE= '/oidc/callback',
        OIDC_SCOPES=["openid", "email", "profile"],
        OIDC_ID_TOKEN_COOKIE_NAME = 'oidc_token',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # register the database commands
    from hotel import db
    db.init_app(app)

    # apply the blueprints to the app
    from hotel import auth, blog, rooms
    app.register_blueprint(rooms.bp)

    # for Okta
    # Ref: https://www.fullstackpython.com/blog/add-user-authentication-flask-apps-okta.html

    from hotel import okta
    with app.app_context():
        okta.init_app(app)



    @app.route('/hello') # For testing factory method
    def hello():
        return 'Hello, World!'


    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app
