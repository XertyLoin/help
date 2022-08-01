from mmap import mmap
import discord
from discord.ext import commands
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from discord_slash.utils.manage_commands import  create_choice, create_option

import sqlite3
from datetime import datetime
import json

from interactions import Overwrite

jsonfile = open("config.json", "r")
jsoncontent = jsonfile.read()
configs = json.loads(jsoncontent)

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name=str(configs['regarde']))
bot = commands.Bot(command_prefix="+", description="Bot by Xerty", intents = intents, activity=activity)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Ready !")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas x/")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("JE crois que tu a oublier quel que chose la")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("Tu n'as pas les permissions pour faire cette commande.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("Oups vous ne pouvez iutilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.reply("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")

@bot.event
async def on_command(ctx):
    with open('logs.txt', 'r') as f:
        content = f.read()
        writefile = open('logs.txt','w')
        
        command = str(ctx.command)
        user = str(ctx.message.author)
        id = str(ctx.message.author.id)
        now = datetime.now()

        time = now.strftime("[%H:%M:%S]")
        date = now.strftime("[%d-%m-%Y]")
        
        newcontent = f"{content}{user} avec l'id : [{id}] a éxécuter la command {command} a {time} le {date}\n"

        writefile.write(newcontent)

@slash.slash(name='mod', description='permet de modérer votre serveur', options=[
    create_option(
        name='quefaire',
        description='que voulait vous faire ?',
        option_type=3,
        required=True,
        choices=[
            create_choice(
                name='create',
                value="c"
            ),
            create_choice(
                name='ban',
                value='b'
            ),
            create_choice(
                name='kick',
                value='k'
            )

        ]

    ),
    create_option(name='createquoi', description='Que voulais vous créer ?', option_type=3, required=False, choices=[
        create_choice(
            name='channel',
            value='cc'
        )
    ]),
    create_option(name='type', description='type channel a créer', option_type=3, required=False, choices=[
        create_choice(
            name='voice',
            value='cv'
        ),
        create_choice(
            name='text',
            value='ct'
        )
    ]),
    create_option(name='name', description='nom du channel', option_type=3, required=False),
    create_option(name='permissions', description='les permissions du channel', option_type=3, required=False, choices=[
        create_choice(
            name='eNoSpeak',
            value='peNoSpeak'
        ),
        create_choice(
            name='eNoSee',
            value='peNoSee'
        )
    ])
])
async def mod(ctx, quefaire=None, createquoi=None, type=None, name=None, permissions=None):
    if quefaire == "c":
        if createquoi == "cc":
            if type == "text":
                if permissions == "peNoSpeak":
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    }
                    await ctx.guild.create_text_channel(name, overwrites=overwrites)
                    await ctx.reply(f"J'ai créer le salon textuel {name} et j'ai fait en sorte que everyone ne peut pas écrire dans se salon")
                elif permissions == "peNoSee":
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
                    }
                    await ctx.guild.create_text_channel(name, overwrites=overwrites)
                else:
                    await ctx.guild.create_text_channel(name)
                    await ctx.reply(f"Le salon textuel {name} a été créer")
            if type == "voice":
                await ctx.guild.create_voice_channel(name)
                await ctx.reply(f"Le salon vocal {name} a été créer")

    if quefaire == "b":
        for mentioned in ctx.message.mentions:
            id = mentioned.id
            member = ctx.guild.get_member(id)
            await member.ban()
            member = str(mentioned)
            await ctx.reply(f"<@{id}> a été ban :hammer:")
    if quefaire == "k":
        for mentioned in ctx.message.mentions:
            id = mentioned.id
            member = ctx.guild.get_member(id)
            await member.kick()
            member = str(mentioned)
            await ctx.reply(f"<@{id}> a été kick :hammer:")

@bot.command()
async def anoucement(ctx, what=None, title=None, nf=None, name1=None, value1=None, name2=None, name3=None, name4=None, name5=None, name6=None, name7=None):
    if what == "quot":
        embed = discord.Embed(title=title)
        for x in range(int(nf)):
            print(title)
            print(name1)
            print(value1)
        #await ctx.send(embed=embed)
    
bot.run(str(configs['token']))