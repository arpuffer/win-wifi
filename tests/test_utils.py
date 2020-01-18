from winwifi.utils import _flatten_kwargs

def test_flatten_kwargs():
    """Flatten simple dict into space separated string"""
    kwargs = {'key1': 'val1', 'key2': 'val2'}
    assert _flatten_kwargs(kwargs) == 'key1 val1 key2 val2'
