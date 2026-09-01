"""Server smoke test: the exported `server` imports and answers over HTTP."""

import pytest

import app as app_module


@pytest.fixture()
def client():
    return app_module.server.test_client()


def test_debug_is_off_by_default():
    assert app_module.server.debug is False


def test_healthz(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.data == b'ok'


def test_index_renders(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Fondamentaux de la conversion' in resp.data


def test_dash_layout_endpoint(client):
    resp = client.get('/_dash-layout')
    assert resp.status_code == 200
    assert resp.is_json


def test_circuit_asset_is_served(client):
    resp = client.get('/assets/case_1.drawio.png')
    assert resp.status_code == 200
    assert resp.mimetype == 'image/png'
