import os
import sys

# ensure package path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from ip_checker import SimpleIPChecker


def test_format_results_error():
    checker = SimpleIPChecker()
    result = {'error': 'fail'}
    formatted = checker.format_results(result)
    assert 'Error' in formatted


def test_format_results_success():
    checker = SimpleIPChecker()
    data = {
        'ip': '1.1.1.1',
        'timestamp': 'now',
        'country': 'US',
        'city': 'NY',
        'region': 'NY',
        'isp': 'ISP',
        'org': 'Org',
        'as': 'AS',
    }
    formatted = checker.format_results(data)
    assert 'IP Address' in formatted
    assert 'ISP' in formatted
