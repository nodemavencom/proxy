import os
import sys

# Add the python package directory to import nodemaven
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from nodemaven.utils import build_proxy_username


def test_country_option():
    result = build_proxy_username('testuser', country='US')
    assert result == 'testuser-country-us-ipv4-true-filter-medium'


def test_city_option():
    result = build_proxy_username('testuser', country='US', city='New York')
    assert result == 'testuser-country-us-city-newyork-ipv4-true-filter-medium'


def test_session_option():
    result = build_proxy_username('testuser', session='abc123')
    assert result == 'testuser-ipv4-true-sid-abc123-filter-medium'

