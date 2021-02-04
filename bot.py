import discord
import asyncio
import sqlite3
from discord.ext import commands
from discord.utils import get

db = sqlite3.connect("./db/sqlite.db")
s = db.cursor()

s.execute("""CREATE TABLE IF NOT EXISTS 
		 Product(_id INTEGER PRIMARY KEY AUTOINCREMENT, name_product TEXT, type_product TEXT,
		 company_product TEXT, model_product TEXT,
		 price_product REAL, count_product INT)""")
db.commit()

prefix = '/'
client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
client.remove_command('help')

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

@client.command(aliases=['add_product'])
async def add_prod(ctx, *args):
	if len(args) == 6:
		if args[5].isdigit() and is_float(args[4]):
			s.execute("""INSERT INTO Product(name_product, type_product,
		 		 	 company_product, model_product,
		 		 	 price_product, count_product) VALUES (?, ?, ?, ?, ?, ?)""", args)
			db.commit()
			await ctx.send(args[0])
		else:
			await ctx.send('Вы указали вместо числа (количества товара или цены) строку.')
	else:
		await ctx.send('Указаны не все аргументы')

@client.command(aliases=['all_info'])
async def all_inf(ctx):
	count = s.execute('SELECT COUNT(*) FROM Product').fetchone()[0]
	for i in range(1, count + 1):
		dat = s.execute('SELECT * FROM Product WHERE _id = (?)', (i,)).fetchall()[0]
		await ctx.send(dat)

@client.event
async def on_ready():
    print('Бот работает.')

@client.event
async def on_message(message):
    msg = message.content.lower()
    await client.process_commands(message)

client.run('NzAwNzMyOTY1NTY2NTQ1OTkw.XpnObQ.7RrZF4ILQgifGKvqRxfCLw-NfcI')