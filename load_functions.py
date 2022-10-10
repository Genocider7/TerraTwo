import json, sys
from command_parsing import *
from constants import what_uses_author, what_uses_channel, what_uses_client, what_uses_message, async_functions

function_file = None
function_dict = {}

def str_to_class(classname : str, module = __name__):
    return getattr(sys.modules[module], classname, None)

def uses_message(commands):
    for command in commands:
        if command['ignore']:
            continue
        if command['type'] in what_uses_message:
            return True
    return False

def uses_author(commands):
    for command in commands:
        if command['ignore']:
            continue
        if command['type'] in what_uses_author:
            return True
    return False

def uses_channel(commands):
    for command in commands:
        if command['ignore']:
            continue
        if command['type'] in what_uses_channel:
            return True
    return False

def uses_client(commands):
    for command in commands:
        if command['ignore']:
            continue
        if command['type'] in what_uses_client:
            return True
    return False

def is_async(commands):
    for command in commands:
        if command['ignore']:
            continue
        if command['type'] in async_functions:
            return True
    return False

def get_req_by_name(req_name):
    for req in function_dict['reqs']:
        if req['name'] == req_name:
            return req
    return False

def get_fun_by_name(fun_name):
    for fun in function_dict['functions']:
        if fun['name'] == fun_name:
            return fun
    return False

def ind(number = 1):
    str = '    '
    ret = ''
    for i in range(number):
        ret += str
    return ret

def load_function_dict(fp):
    global function_dict
    function_json_file = open(fp, "r")
    function_dict = json.loads(function_json_file.read())
    function_json_file.close()

def write_function_def(req_fun, function_file):
    if is_async(req_fun['commands']):
        function_file.write('async ')
    function_file.write('def ' + req_fun['name'] + '(ctx):\n')

def write_local_vars(req_fun, function_file):
    if uses_message(req_fun['commands']):
        function_file.write(ind() + '_message = ctx[\'message\']\n')
    if uses_author(req_fun['commands']):
        function_file.write(ind() + '_author = ctx[\'author\']\n')
    if uses_channel(req_fun['commands']):
        function_file.write(ind() + '_channel = ctx[\'channel\']\n')
    if uses_client(req_fun['commands']):
        function_file.write(ind() + '_client = ctx[\'client\']\n')

def create_requirements():
    for req in function_dict['reqs']:
        write_function_def(req, function_file)
        write_local_vars(req, function_file)
        for command in req['commands']:
            if command['ignore']:
                continue
            command_class = str_to_class(command['type'], 'command_parsing')
            if command_class != None:
                command_class.write_command(command, function_file)
        function_file.write(ind() + 'return True\n\n')

def create_functions():
    for fun in function_dict['functions']:
        write_function_def(fun, function_file)
        write_local_vars(fun, function_file)
        for command in fun['commands']:
            if command['ignore']:
                continue
            command_class = str_to_class(command['type'], 'command_parsing')
            if command_class != None:
                command_class.write_command(command, function_file)
        function_file.write('\n')

def create_commands():
    function_file.write('commands = [\n')
    for command in function_dict['commands']:
        function_file.write(ind() + '{\n')
        if not command['description'] == '':
            function_file.write(ind(2) + '#' + command['description'] + '\n')
        function_file.write(ind(2) + '\'req\': ' + command['req_name'] + ',\n')
        function_file.write(ind(2) + '\'function\': ' + command['fun_name'] + ',\n')
        function_file.write(ind(2) + '\'req_cor\': ')
        temp_req = get_req_by_name(command['req_name'])
        if temp_req == False:
            raise Exception('Req name not found')
        if is_async(temp_req['commands']):
            function_file.write('True,\n')
        else:
            function_file.write('False,\n')
        function_file.write(ind(2) + '\'fun_cor\': ')
        temp_fun = get_fun_by_name(command['fun_name'])
        if temp_fun == False:
            raise Exception('Function name not found')
        if is_async(temp_fun['commands']):
            function_file.write('True\n')
        else:
            function_file.write('False\n')
        function_file.write(ind() + '},\n')
    function_file.write(']')

def main():
    global function_file
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " filepath")
        return
    load_function_dict(sys.argv[1])
    function_file = open('functions.py', 'w')
    create_requirements()
    create_functions()
    create_commands()
    function_file.close()

if __name__ == "__main__":
    main()
