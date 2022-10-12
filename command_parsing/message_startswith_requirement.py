#Wymóg do eventu on_message

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\share")
from functions_shared import escape_message_string, ind

def write_command(command, function_file):
    function_file.write(ind() + 'if ')
    if not command['negation']:
        function_file.write('not ')
    function_file.write('_message')
    if not command['case_sensitive']:
        function_file.write('.lower()')
    function_file.write('.startswith(')
    if command['args'][0]['type'] == 'string':
        escaped_command = escape_message_string(command['args'][0]['content'])
        function_file.write(escaped_command)
    else:
        function_file.write('str(' + command['args'][0]['content'] + ')')
    if not command['case_sensitive']:
        function_file.write('.lower()')
    function_file.write('):\n')
    function_file.write(ind(2) + 'return False\n')
