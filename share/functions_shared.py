def escape_message_string(message : str):
    escaped_message = message.replace("\\", "\\\\")
    escaped_message = escaped_message.replace("\"", "\\\"")
    escaped_message = escaped_message.replace("t2{message}", "\" + _message + \"")
    escaped_message = escaped_message.replace("t2{author_name}", "\" + _author.display_name + \"")
    return "\"" + escaped_message + "\""