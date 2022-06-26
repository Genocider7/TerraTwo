import discord

def req1(ctx):
    message = ctx['message']
    author = ctx['author']
    if not message.lower().startswith('?off'):
        return False
    if not author.id == 330392410964361217:
        return False
    return True

async def fun1(ctx):
    client = ctx['client']
    await client.close()

commands = [
    {
        #turning off bot
        'req': req1,
        'function': fun1,
        'req_cor': False,
        'fun_cor': True
    },
]