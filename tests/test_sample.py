import os


def my_function(src_dir):
    """This is the function we're testing.  executes 'ls some_dir/' in bash."""
    os.system('ls ' + src_dir)
    
@unittest.mock.patch('os.system')  # This declares that we are mocking the os.system call made by my_function()
def test_my_function(os_system):  # The input to the test function is the mocked os.system (you can name this anything, it's set up by the decorator above, but it's smart to name it sensibly)
    # type: (unittest.mock.Mock) -> None
    my_function("/path/to/dir")
    os_system.assert_called_once_with('ls /path/to/dir')  # os_system is a python unittest MagicMock object that behaves like the function it mocks, but also has inherited methods from MagicMock, like the assert_called_with you see here
