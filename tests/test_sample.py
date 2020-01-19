import os


def my_function(src_dir):
    os.system('ls ' + src_dir)
    
@unittest.mock.patch('os.system')
def test_my_function(os_system):
    # type: (unittest.mock.Mock) -> None
    my_function("/path/to/dir")
    os_system.assert_called_once_with('ls /path/to/dir')
