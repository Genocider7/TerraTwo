def write_command(command, function_file):
    function_file.write('    if ')
    if not command['negation']:
        function_file.write('not ')
    function_file.write('_message')
    if not command['case_sensitive']:
        function_file.write('.lower()')
    function_file.write('.startswith(')
    if command['args'][0]['type'] == 'string':
        function_file.write('\'' + command['args'][0]['content'] + '\'')
    else:
        function_file.write('str(' + command['args'][0]['content'] + ')')
    if not command['case_sensitive']:
        function_file.write('.lower()')
    function_file.write('):\n')
    function_file.write('        return False\n')