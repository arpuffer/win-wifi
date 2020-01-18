def _flatten_kwargs(kwargs: dict):
    return ' '.join('%s %s' % (k, v) for (k, v) in kwargs.items())