import discord

client = discord.Client()

activity = discord.Game(name="Mafioso")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=activity)


help_text = [
    "```List of commands```",
    "Type t!help [command] to receive details about the command itself.",
    "**1. Basic**: `help` `h2p` `start` `end`",
        # refers to itself, how to play, start game, end game (only mod or player)
    "**2. Setup**: `roles` `add` `remove` `setup` `settings` `toggle` `join` `leave`",
        # see all roles, add/remove role, check current setup
    "**3. In-game**: `vote` `unvote` `status` `players` `alive`"
        # vote [player], unvote, who is voting whom, alive players, alive roles
]

h2p_text = [
    "**How to play:**",
    "Mafia is a party game in which all the players are split into two opposing factions: the innocent villagers and the guilty mafia.\n",
    "The game alternates between two phases:",
    "1. Daytime, when players can discuss and debate the identity of the mafia. Players can also majority vote to lynch one member of the community who they suspect of being guilty.",
    "2. Nighttime, when mafia are free to murder one innocent citizen of the town, and certain townspeople can use their special abilities.\n",
    "If you are a villager, your win condition is to identify and lynch all of the mafia.",
    "If you are a mafia, your win condition is to either equal or outnumber the townspeople.",
    "At the start of the game, your role will be assigned to you via DM by this bot."
]

commands = {
    'help': '`m!help` displays the help screen. Fairly obvious.',
    'h2p': '`m!h2p` describes the basic rules and premise of the game.',
    'start': '`m!start` begins a new round of mafia.',
    'end': '`m!end` ends the current game, if existing. Can only be called by a moderator or a player.',
    'roles': '`m!roles` lists all available roles that can be added to the game.',
    'add': '`m!add [role] [number]` adds `[number]`x of `[role]` to the current setup.',
    'remove': '`m!remove [role] [number]` removes `[number]`x of [role] from the current setup.',
    'setup': '`m!setup` shows the full complement of roles in the current setup.',
    'settings': '`m!settings` displays all the settings of the current game.',
    'toggle': '`m!toggle [setting]` flips `[setting]` from true to false, or vice versa. Do `m!settings` to see options',
    'join' : '`m!join` makes you join the game.',
    'leave' : '`m!leave` makes you leave the game.',
    'vote': '`m!vote [player]` puts your current vote on `player`.',
    'unvote': '`m!unvote` sets your vote to nobody (no vote).',
    'status': '`m!status` displays all players and their votes, as well as current voting leaders.',
    'players': '`m!players` displays all players who are currently alive',
    'alive': '`m!alive` displays all the roles and their quantities that are still in play.'
}


settings = {
    'daystart': 0,      # game starts during daytime
    'selfsave': 0,      # doctor can save themselves
    'conssave': 0,      # doctor can save the same person in consecutive turns
    'paritycop': 0,     # parity cop if true (gets reports on if people are aligned the same way)
    'limit1': 'inf',    # time limit for days
    'limit2': 'inf'     # time limit for nights
}


toggle_text = [{
    'daystart': 'daystart toggled off: The game will commence during nighttime.',
    'selfsave': 'selfsave toggled off: The doctor will not be able to save himself during nighttime.',
    'conssave': 'conssave toggled off: The doctor will not be able to save the same patient over consecutive nights.',
    'paritycop': 'paritycop toggled off: The cop will receive a report stating the alignment of the target (innocent or guilty)'
}, {
    'daystart': 'daystart toggled on: The game will commence during daytime.',
    'selfsave': 'selfsave toggled on: The doctor will be able to save himself during nighttime.',
    'conssave': 'conssave toggled on: The doctor will be able to save the same patient over consecutive nights.',
    'paritycop': 'paritycop toggled on: The cop will receive a report stating if his LAST TWO targets are of the same alignment or not.'
}]


async def invalid(message):
    await message.channel.send('Invalid request. Please refer to `m!help` for aid.')

async def m_help(message):
    query = message.content.split()
    if len(query) == 1:
        await message.channel.send('\n'.join(help_text))
    elif len(query) == 2 and query[1] in commands:
        await message.channel.send(commands[query[1]])
    else:
        await invalid(message)

async def m_h2p(message):
    await message.channel.send('\n'.join(h2p_text))

async def m_start(message):
    pass

async def m_end(message):
    pass

async def m_roles(message):
    pass

async def m_add(message):
    pass

async def m_remove(message):
    pass

async def m_setup(message):
    pass

async def m_settings(message):
    await message.channel.send('\n'.join([key+str(": ")+str(settings[key]) for key in settings]))

async def m_toggle(message):
    query = message.content.split()
    if query[1] in settings:
        if query[1] == 'limit1' or query[1] == 'limit2':
            if query[2] == 'inf':
                settings[query[1]] = query[2]
                if query[1] == 'limit1':
                    await message.channel.send('Time limit for day set to infinite minutes.')
                else:
                    await message.channel.send('Time limit for night set to infinite minutes.')
            else:
                try:
                    settings[query[1]] = float(query[2])
                    if query[1] == 'limit1':
                        await message.channel.send('Time limit for day set to '+query[2]+' minutes.')
                    else:
                        await message.channel.send('Time limit for night set to '+query[2]+' minutes.')
                except:
                    await invalid(message)
        else:
            settings[query[1]] ^= 1
            await message.channel.send(toggle_text[settings[query[1]]][query[1]])
        return
    await invalid(message)

async def m_join(message):
    pass

async def m_leave(message):
    pass

async def m_vote(message):
    pass

async def m_unvote(message):
    pass

async def m_status(message):
    pass

async def m_players(message):
    pass

async def m_alive(message):
    pass


tofunc = {
    'help' : m_help, 'h2p': m_h2p, 'start': m_start,
    'end': m_end, 'roles': m_roles, 'add': m_add,
    'remove': m_remove, 'setup': m_setup, 'settings': m_settings,
    'toggle': m_toggle, 'vote': m_vote, 'unvote': m_unvote,
    'status': m_status, 'players': m_players, 'alive': m_alive
}


@client.event
async def on_message(message):
    if message.author == client.user or len(message.content) < 2 or message.content[:2] != 'm!':
        return
    query = message.content[2:].split()
    if len(query) and query[0] in commands:
        func = tofunc[query[0]]
        await func(message)
    else:
        await invalid(message)





client.run('NTk0MTg0ODU4MTM4NTc0ODQ4.XRYvzw._Y6KIxJ0G9BpKd6ORpj2Uhtpmpg')