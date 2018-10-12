# Discord bot for it's B-time
# Nicknamed "Kakarot"
import configparser
import discord

version = "0.01-kakarot"

config = configparser.ConfigParser()

config.read('config.ini')

TOKEN = config['CREDENTIALS']['token']
watched_channel = config['CHANNELS']['WatchedChannel']
announce_channel_tts = config['CHANNELS']['AnnounceChannelTTS']

client = discord.Client()

# Get all channels in server
announce_channel_list = []
for server in client.servers:
    for channel in server.channels:
        if channel.type == 'text' and channel.name == 'general':
            announce_channel_list.append(channel)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print(client.user.name + ' started and connected')
    print('------')

# TODO: Make use of voice functions instead of TTS announce channel
@client.event
async def on_voice_state_update(before, after):
	# TODO: Check that VoiceStateUpdate change type is actually joining server, not ANY change
    if after.voice.voice_channel is not None and after.voice.voice_channel.name == 'Is gaem tim':
        for channel in after.server.channels:
            if channel.name == watched_channel:
                for channel2 in after.server.channels:
                    if str(channel2.type) == 'text' and channel2.name == announce_channel_tts:
                        await client.send_message(channel2, f"{before.name} joined", tts=True)
	
client.run(TOKEN)