from oauth2client.client import OAuth2Credentials
from flask_oidc import OpenIDConnect
from okta import UsersClient

import click
from flask import current_app, g, session
from flask.cli import with_appcontext

oidc = OpenIDConnect()


def get_oidc():
    """
    Connect to okta
    """
    if 'oidc' not in g:
        print('okta: get_oidc call')
        g.oidc = OpenIDConnect(current_app)
        g.okta_client = UsersClient("https://dev-833144.okta.com", "00xJ6vTQkI8LzIQcPXf7Ehw75GrdAVDdqA2tvQFxFx")
        # fixing global oidc problem for decorator in rooms
        oidc = g.oidc
    return g.oidc


def close_oidc(app):
    """ Release okta connection
    """
    oidc = g.pop('oidc',None)
    if oidc is not None:
        oidc.logout()
    
    # with app.app_context():
    #     session.clear()


def init_okta():
    """Connect to existing table"""
    oidc = get_oidc()
    """ Can do additional initialization if required """


@click.command('init-okta')
@with_appcontext
def init_okta_command():
    """Connect to existing oidc"""
    init_okta()
    click.echo (get_oidc())
    click.echo('Initialized Okta.')
    print('Initialized Okta.')


def init_app(app):
    """Register Okta functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_oidc)
    app.cli.add_command(init_okta_command)