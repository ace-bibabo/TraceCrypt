from termcolor import colored
import shutil

dbf_life_cycle = 9 * 60  # DBF that is older than 9 min from the current time is deleted from the node’s storage.
BACKEND_SERVER_PORT = 55000
BACKEND_SERVER_IP = '127.0.0.1'



def print_colored(text, color='white', attrs=None):
    """Prints text with the specified color using termcolor."""
    print(colored("=" * shutil.get_terminal_size().columns, 'white'))
    print(colored(text, color, attrs=attrs))
