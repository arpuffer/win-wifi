from winwifi.utils import flatten_kwargs

def test_flatten_kwargs():
    kwargs = {'key1': 'val1', 'key2': 'val2'}
    assert flatten_kwargs(kwargs) == 'key1 val1 key2 val2'
