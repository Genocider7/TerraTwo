class conv_requirement
{
    constructor(name) 
    {
        this.name = name;
        this.commands = [];
    }
}

class conv_function
{
    constructor(name)
    {
        this.name = name;
        this.commands = [];
    }
}

class conv_command
{
    constructor(req, fun)
    {
        this.description = "";
        this.req = req;
        this.fun = fun;
    }

    constructor(desc, req, fun)
    {
        this.description = desc;
        this.req = req;
        this.fun = fun;
    }
}

class reqfun_command 
{
    constructor(type) 
    {
        this.type = type;
        this.ignore = true;
    }
}

class message_startswith_requirement extends reqfun_command
{
    constructor(arg)
    {
        super("message_startswith_requirement")
        this.negation = false;
        this.case_sensitive = false;
        this.args = [arg];
    }

    constructor(type, content)
    {
        super("message_startswith_requirement")
        this.negation = false;
        this.case_sensitive = false;
        this.args = [new command_arg(type, content)];
    }
}

class author_id_requirement extends reqfun_command
{
    constructor(arg)
    {
        super("author_id_requirement")
        this.negation = false;
        this.args = [arg];
    }

    constructor(type, content)
    {
        super("author_id_requirement")
        this.negation = false;
        this.args = [new command_arg(type, content)];
    }
}

class client_logout extends reqfun_command
{
    constructor()
    {
        super("client_logout");
    }
}

class send_message extends reqfun_command
{
    constructor(arg1, arg2)
    {
        super("send_message");
        this.args = [arg1, arg2];
    }

    constructor(channel_type, channel, message_type, message)
    {
        super("send_message");
        this.args =[
            new command_arg(channel_type, channel),
            new command_arg(message_type, message)
        ];
    }
}

class command_arg
{
    constructor(type, content)
    {
        this.type = type;
        this.content = JSON.stringify(content);
    }
}