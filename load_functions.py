import json, sys

what_uses_message = ['message_startswith_requirement', 'custom']
what_uses_author = ['author_id_requirement', 'custom']
what_uses_channel = ['custom']
what_uses_client = ['client_logout', 'custom']
async_functions = ['client_logout', 'custom']

function_dir = {}

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
    for req in function_dir['reqs']:
        if req['name'] == req_name:
            return req
    return False

def get_fun_by_name(fun_name):
    for fun in function_dir['functions']:
        if fun['name'] == fun_name:
            return fun
    return False

def ind(number = 1):
    str = '    '
    ret = ''
    for i in range(number):
        ret += str
    return ret

def create_functions_from_file(fp):
    global function_dir
    function_json_file = open(fp, "r")
    function_dir = json.loads(function_json_file.read())
    function_json_file.close()

    function_file = open('functions.py', 'w')

    for req in function_dir['reqs']:
        if is_async(req['commands']):
            function_file.write('async ')
        function_file.write('def ' + req['name'] + '(ctx):\n')
        if uses_message(req['commands']):
            function_file.write(ind() + '_message = ctx[\'message\']\n')
        if uses_author(req['commands']):
            function_file.write(ind() + '_author = ctx[\'author\']\n')
        if uses_channel(req['commands']):
            function_file.write(ind() + '_channel = ctx[\'channel\']\n')
        if uses_client(req['commands']):
            function_file.write(ind() + '_client = ctx[\'client\']\n')
        for command in req['commands']:
            if command['ignore']:
                continue

            if command['type'] == 'message_startswith_requirement':
                function_file.write(ind() + 'if ')
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
                function_file.write(ind(2) + 'return False\n')

            elif command['type'] == 'author_id_requirement':
                function_file.write(ind() + 'if ')
                if not command['negation']:
                    function_file.write('not ')
                function_file.write('_author.id == ')
                if command['args'][0]['type'] == 'int':
                    function_file.write(command['args'][0]['content'] + ':\n')
                elif command['args'][0]['type'] == 'string':
                    function_file.write('int(\'' + command['args'][0]['content'] + '\'):\n')
                else:
                    function_file.write('int(' + command['args'][0]['content'] + '):\n')
                function_file.write(ind(2) + 'return False\n')

            #elif command['type'] == ...
        function_file.write(ind() + 'return True\n\n')


    for fun in function_dir['functions']:
        if is_async(fun['commands']):
            function_file.write('async ')
        function_file.write('def ' + fun['name'] + '(ctx):\n')
        if uses_message(fun['commands']):
            function_file.write(ind() + '_message = ctx[\'message\']\n')
        if uses_author(fun['commands']):
            function_file.write(ind() + '_author = ctx[\'author\']\n')
        if uses_channel(fun['commands']):
            function_file.write(ind() + '_channel = ctx[\'channel\']\n')
        if uses_client(fun['commands']):
            function_file.write(ind() + '_client = ctx[\'client\']\n')
        for command in fun['commands']:
            if command['ignore']:
                continue

            if command['type'] == 'client_logout':
                function_file.write(ind() + 'await _client.close()\n')

            #elif command['type'] == ...
        function_file.write('\n')

    function_file.write('commands = [\n')
    for command in function_dir['commands']:
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

    function_file.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " filepath")
        return
    create_functions_from_file(sys.argv[1])

if __name__ == "__main__":
    main()