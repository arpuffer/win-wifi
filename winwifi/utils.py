'''
Copyright (c) 2020 Alex Puffer. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
'''

def _flatten_kwargs(kwargs: dict):
    return ' '.join('%s %s' % (k, v) for (k, v) in kwargs.items())