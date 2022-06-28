def write_command(command, function_file):
    function_file.write('    await _client.close()\n')
