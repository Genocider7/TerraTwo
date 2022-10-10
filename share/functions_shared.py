import re

def escape_message_string(message : str):
    escaped_message = message.replace("\\", "\\\\")
    escaped_message = escaped_message.replace("\"", "\\\"")
    escaped_message = escaped_message.replace("t2{author_name}", "\" + _author.display_name + \"")
    matches = re.findall(r't2{message(\[\d*:-?\d*\])?}', escaped_message)
    for match in matches:
        escaped_message = escaped_message.replace("t2{message" + match + "}", "\" + _message" + match + " + \"")
    return "\"" + escaped_message + "\""