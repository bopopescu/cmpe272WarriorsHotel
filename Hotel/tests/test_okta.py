import pytest
from hotel.okta import get_oidc


def test_get_close_db(app):
    with app.app_context():
        oidc = get_oidc()
        assert oidc is get_oidc()

def test_init_okta_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_okta():
        Recorder.called = True

    monkeypatch.setattr('hotel.okta.init_okta', fake_init_okta)
    result = runner.invoke(args=['init-okta'])
    assert 'Initialized' in result.output
    assert Recorder.called
