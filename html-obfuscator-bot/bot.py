import discord
import time
import os
import urllib.parse

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

if not os.path.exists('obfuscated'):
    os.makedirs('obfuscated')

# Config:

config_token = ""                       # REQUIRED : Your discord bottoken

config_thumbnail_url = ""
config_icon_url = ""
config_failtitle = "**FAILURE**"
config_footer = "© onkelseo 2022"
config_watermark = "<!-- MADE BY onkelseo\n-- OBFUSCATE WITH onkelseo-html-obfuscator -->\n\n"

config_nofile = "Please attach a file!"
config_nohtmlfile = "Please attach an HTML file!"
config_obf_success = "**Here is your obfuscated code!**"

config_obf_cmd = "!obfuscatehtml"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config_obf_cmd):
        if len(message.attachments) == 0:

            embed = discord.Embed(title=config_failtitle, description=config_nofile, color=discord.Color.red())
            embed.set_footer(text=config_footer, icon_url=config_icon_url)
            embed.set_thumbnail(url=config_thumbnail_url)
            await message.channel.send(embed=embed)
            return


        attachment = message.attachments[0]
        if not attachment.filename.lower().endswith('.html'):

            embed = discord.Embed(title=config_failtitle, description=config_nohtmlfile, color=discord.Color.red())
            embed.set_footer(text=config_footer, icon_url=config_icon_url)
            embed.set_thumbnail(url=config_thumbnail_url)
            await message.channel.send(embed=embed)
            return

        attachment_content = await attachment.read()

        code = attachment_content.decode('utf-8')

        obfuscated_code = obfuscate_html(code)


        obfuscated_code = f'{config_watermark}\n{obfuscated_code}'

        timestamp = int(time.time())
        filename = f'obfuscated/obfuscated_{timestamp}.html'
        original_filename = f'obfuscated/original_{timestamp}.html'

        with open(original_filename, 'w', encoding='utf-8') as f:
            f.write(code)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)

        obfuscated_file = discord.File(filename)
        response = f"{config_obf_success}"

        await message.channel.send(response, file=obfuscated_file)

def obfuscate_html(html):

    obfuscated = '<script>\n'
    obfuscated += 'document.write(unescape(\''
    obfuscated += urllib.parse.quote(html, safe='')
    obfuscated += '\'))\n'
    obfuscated += '</script>\n'

    return obfuscated



client.run(config_token)
