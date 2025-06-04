import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

import quick_test


def test_test_proxy_connection_success():
    with mock.patch('quick_test.get_current_ip', return_value='1.2.3.4'):
        result = quick_test.test_proxy_connection('desc', {'http': 'url'})
        assert result is True


def test_test_proxy_connection_failure():
    with mock.patch('quick_test.get_current_ip', return_value=None):
        result = quick_test.test_proxy_connection('desc', {'http': 'url'})
        assert result is False
