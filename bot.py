import asyncio
from datetime import time
import discord
from discord import activity
from discord.ext import commands
from discord.ext.commands import Bot, bot
import asyncio
from discord import Activity, ActivityType
import json
import os

Bot = commands.Bot(command_prefix= "!")

@Bot.command()
async def say(ctx,arg):
    await ctx.send(arg)

@Bot.command()
async def info(ctx,member:discord.Member):
    emb = discord.Embed(title='Информация о пользователе:',color=0xff0000)
    emb.add_field(name="Когда присоединился:", value=member.joined_at,inline=False)
    emb.add_field(name="Имя:",value=member.display_name,inline=False)
    emb.add_field(name="Айди: ",value=member.id,inline=False)
    emb.add_field(name="Аккаунт был создан: ",value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"),inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    emb.set_footer(text=f"Вызвано: {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    emb.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed = emb)


@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def mute(ctx,member:discord.Member,time:int,reason):
    channel = Bot.get_channel(863248127028625479)
    muterole = discord.utils.get(ctx.guild.roles, id=863239629284311050)
    emb = discord.Embed(title="Мут",color=0xff0000)
    emb.add_field(name="Модератор",value=ctx.message.author.mention,inline=False)
    emb.add_field(name="Нарушитель",value=member.mention,inline=False)
    emb.add_field(name="Причина",value=reason,inline=False)
    emb.add_field(name="Время",value=time,inline=False)
    await member.add_roles(muterole)
    await channel.send(embed = emb)
    await asyncio.sleep(time * 60)
    await member.remove_roles(muterole)


@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def unmute(ctx,member:discord.Member):
    channel = Bot.get_channel(863248127028625479)
    muterole = discord.utils.get(ctx.guild.roles, id=863239629284311050)
    emb = discord.Embed(title="Снятие мута",color=0xff0000)
    emb.add_field(name="Модератор",value=ctx.message.author.mention,inline=False)
    emb.add_field(name="Нарушитель",value=member.mention,inline=False)
    await channel.send(embed = emb)
    await member.remove_roles(muterole)

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def kick(ctx,member:discord.Member,reason):
    channel = Bot.get_channel(863248127028625479)
    emb = discord.Embed(title="Кик",color=0xff0000)
    emb.add_field(name="Модератор",value=ctx.message.author.mention,inline=False)
    emb.add_field(name="Нарушитель",value=member.mention,inline=False)
    emb.add_field(name="Причина",value=reason,inline=False)
    await member.kick()
    await channel.send(embed = emb)

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def ban(ctx,member:discord.Member,reason):
    channel = Bot.get_channel(863248127028625479)
    emb = discord.Embed(title="Бан",color=0xff0000)
    emb.add_field(name="Модератор",value=ctx.message.author.mention,inline=False)
    emb.add_field(name="Нарушитель",value=member.mention,inline=False)
    emb.add_field(name="Причина",value=reason,inline=False)
    emb.add_field(name="Время",value=time,inline=False)
    await member.ban(reason)
    await channel.send(embed = emb)

@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def clear(ctx,amount=10):
    deleted = await ctx.message.channel.purge(limit=amount+1)

@Bot.event
async def on_ready():
    print("Бот запустился")
    await Bot.change_presence(status=discord.Status.idle,activity=Activity(name="за MagicRP#1 connect 212.22.93.178:27016", type=ActivityType.watching))

@Bot.event
async def on_voice_state_update(member,before,after):
    if after.channel.id == 863177452025020450:
        for guild in Bot.guilds:
            maincategory = discord.utils.get(guild.categories, id=863177452025020450)
            channel2 = await guild.create_voice_channel(name=f"канал {member.display_name}",category = maincategory)
            await channel2.set_permissions(member,connect=True, mute_members=True, move_members=True, manage_channels=True)
            await member.move_to(channel2)
            def check(x,y,z):
                return len(channel2.members) == 0
            await Bot.wait_for("voice_state_update",check=check)
            await channel2.delete()
 










token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
