import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\share")
from functions_shared import escape_message_string

def write_command(command, function_file):
    if command['args'][0]['type'] == "reply":
        function_file.write("    target_channel = _channel\n")
    elif command['args'][0]['type'] == "int":
        function_file.write("    target_channel = await _client.fetch_channel(" + command['args'][0]['content'] + ")\n")
    elif command['args'][0]['type'] == "string":
        function_file.write("    target_channel = await _client.fetch_channel(int(\"" + command['args'][0]['content'] + "\"))\n")
    if (command['args'][1]['type'] == "string"):
        escaped_message = escape_message_string(command['args'][1]['content'])
    function_file.write("    await target_channel.send(" + escaped_message + ")\n")