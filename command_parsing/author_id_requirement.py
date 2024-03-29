#Wymóg do eventu on_message

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\share")
from functions_shared import ind

def write_command(command, function_file):
    function_file.write(ind() + 'if ')
    if not command['negation']:
        function_file.write('not ')
    function_file.write('_author.id == ')
    if command['args'][0]['type'] == 'int':
        function_file.write(command['args'][0]['content'] + ':\n')
    elif command['args'][0]['type'] == 'string':
        function_file.write("int(\"" + command['args'][0]['content'] + "\"):\n")
    else:
        function_file.write('int(' + command['args'][0]['content'] + '):\n')
    function_file.write(ind(2) + 'return False\n')
