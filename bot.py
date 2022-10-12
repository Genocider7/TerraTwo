import discord
from functions import commands

intents = discord.Intents.default()
client = discord.Client(
    max_messages = None,
    intents = intents
)
TOKEN = None

def get_token_from_file(fp):
    global TOKEN
    file = open(fp, 'r')
    TOKEN = file.read()    
    file.close()

@client.event
async def on_message(message):
    ctx = {
        'message': message.content,
        'author': message.author,
        'client': client,
        'channel': message.channel
    }
    for command in commands:
        if command['event'] != 'on_message':
            continue
        if (command['req_cor']):
            activated = await command['req'](ctx)
        else:
            activated = command['req'](ctx)
        if activated and command['fun_cor']:
            await command['function'](ctx)
        elif activated:
            command['function'](ctx)

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)

if __name__ == '__main__':
    get_token_from_file('TOKEN')
    if (TOKEN != None):
        client.run(TOKEN)
    else:
        raise Exception('Couldn\'t retrieve token')