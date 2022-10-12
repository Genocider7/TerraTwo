#funkcja niezależna od eventu

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\share")
from functions_shared import ind

def write_command(command, function_file):
    function_file.write(ind() + 'await _client.close()\n')
