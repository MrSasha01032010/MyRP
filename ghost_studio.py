import discord
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True

def has_permission(ctx):
    allowed_users = [714891798698524732, 735842572651724870, 992768373047967846]
    if ctx.author.id not in allowed_users:
        asyncio.create_task(ctx.author.send("У вас нет доступа к команде."))
        return False
    return True

bot = commands.Bot(command_prefix='/', intents=intents)

channel_id = 1074364271372279990
event_channel_id = 1211642821010915359

participants = set()

@bot.command()
@commands.check(has_permission)
async def role_send(ctx):
    if not has_permission(ctx):
        return
    
    channel = bot.get_channel(channel_id)
    if channel is None:
        return await ctx.send("Текстовый канал не найден.")
    
    embed = discord.Embed(
        title="Выберите роль:",
        description="Нажмите соответствующую эмодзи, чтобы получить роль.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Роль 1", value="1️⃣", inline=True)
    embed.add_field(name="Роль 2", value="2️⃣", inline=True)
    embed.add_field(name="Роль 3", value="3️⃣", inline=True)
    embed.add_field(name="Роль 4", value="4️⃣", inline=True)
    
    message = await channel.send(embed=embed)
    
    for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']:
        await message.add_reaction(emoji)

@bot.command()
@commands.check(has_permission)
async def adminshaveghots(ctx):
    allowed_role_id = 1027994783819513907
    member = ctx.author
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=allowed_role_id)
    if role is not None:
        await member.add_roles(role)
        await ctx.send(f"Роль {role.name} добавлена.")
    else:
        await ctx.send("Роль не найдена.")

@bot.command()
@commands.check(has_permission)
async def event(ctx, action: str, *, event_type: str):
    if action == 'start':
        if event_type.lower() == 'easy':
            await start_event(ctx)
        else:
            await ctx.send("Неверный тип мероприятия. Доступные типы: easy")
    elif action == 'stop':
        if event_type.lower() == 'easy':
            await stop_event(ctx)
        else:
            await ctx.send("Неверный тип мероприятия. Доступные типы: easy")
    else:
        await ctx.send("Неверное действие. Доступные действия: start, stop")

async def start_event(ctx):
    global participants
    participants = set()
    channel = bot.get_channel(event_channel_id)
    if channel is None:
        return await ctx.send("Канал для мероприятия не найден.")
    
    embed = discord.Embed(
        title="Уникальный конкурс!",
        description="@everyone, СЕЙЧАС ПРОХОДИТ УНИКАЛЬНАЯ КОНКУРС!\n\n**ПРИЗ:**\nДонат ʟᴜɴᴀʀ (2449 рублей)\n\n**ЧТО НУЖНО ДЛЯ УЧАСТИЯ?**\nВсего нажать на эмодзи \"🎉\"",
        color=discord.Color.green()
    )
    message = await channel.send(embed=embed)
    await message.add_reaction("🎉")

async def stop_event(ctx):
    global participants
    channel = bot.get_channel(event_channel_id)
    if channel is None:
        return await ctx.send("Канал для мероприятия не найден.")
    
    winner = random.choice(list(participants))
    winner_member = ctx.guild.get_member(winner)
    if winner_member:
        winner_name = winner_member.display_name
    else:
        winner_name = "Неизвестно"
    
    embed = discord.Embed(
        title="Победитель конкурса!",
        description=f"Поздравляем {winner_name} с победой!",
        color=discord.Color.gold()
    )
    await channel.send(embed=embed)

    participants = set()

@bot.event
async def on_raw_reaction_add(payload):
    global participants
    if payload.channel_id == event_channel_id:
        participants.add(payload.user_id)

bot.run('MTIxMjE1NjkwMzkyNTIyNzU2MQ.GLrnbM.0JTIroQN9s_YX_vqFf4Fpgjpud3h7Txba0As')