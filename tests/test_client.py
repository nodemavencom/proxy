import os
import sys
from unittest import mock

# ensure package path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from nodemaven.client import NodeMavenClient


def test_client_initialization_env(monkeypatch):
    monkeypatch.setenv('NODEMAVEN_APIKEY', 'testkey')
    client = NodeMavenClient()
    assert client.api_key == 'testkey'
    assert client.base_url.endswith('dashboard.nodemaven.com')


def test_client_custom_params():
    client = NodeMavenClient(api_key='a', base_url='https://example.com', timeout=5)
    assert client.api_key == 'a'
    assert client.base_url == 'https://example.com'
    assert client.timeout == 5
