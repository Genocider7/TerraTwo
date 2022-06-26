def req1(ctx):
    _message = ctx['message']
    _author = ctx['author']
    if not _message.lower().startswith('?off'.lower()):
        return False
    if not _author.id == 330392410964361217:
        return False
    return True

async def fun1(ctx):
    _client = ctx['client']
    await _client.close()

commands = [
    {
        #turning off bot
        'req': req1,
        'function': fun1,
        'req_cor': False,
        'fun_cor': True
    },
]