import aiohttp, time, json, sys, logging, logging.handlers

from datetime import datetime
from pprint import saferepr

import discord
from discord.ext import commands

description = """
A.C.E. - Autonomous Command Executor

Written by: RUNIE 🔥#9646
Avatar artwork: Vinter Borge
Contributors: Cap'n Odin#8812 and GeekDude#2532
"""

extensions = (
	'cogs.admin',
	'cogs.mod',
	'cogs.commands',
	'cogs.highlighter',
	'cogs.tags',
	'cogs.reps',
	'cogs.votes',
	'cogs.muter',
	'cogs.roles',
	'cogs.welcome',
	'cogs.guilds.autohotkey',
	'cogs.guilds.dwitter'
)

class AceBot(commands.Bot):
	def __init__(self):

		# setup logger
		self.logger = logging.getLogger('AceBot')
		self.logger.setLevel(logging.INFO)

		fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

		stream = logging.StreamHandler(sys.stdout)
		stream.setLevel(logging.INFO)
		stream.setFormatter(fmt)

		file = logging.handlers.TimedRotatingFileHandler('logs/log.log', when='midnight', encoding='utf-8-sig')
		file.setLevel(logging.INFO)
		file.setFormatter(fmt)

		self.logger.addHandler(stream)
		self.logger.addHandler(file)

		self.logger.info(f'Startup...')

		# load config file
		with open('data/config.json', 'r', encoding='utf-8-sig') as f:
			self.config = json.loads(f.read())

		# init bot
		super().__init__(command_prefix=self.config['prefix'], description=description)

		self.owner_id = 265644569784221696
		self.session = aiohttp.ClientSession(loop=self.loop)

		with open('data/ignore.json', 'r', encoding='utf-8-sig') as f:
			self.ignore_users = json.loads(f.read())

		# check for ignored users and bots
		self.add_check(self.blacklist_ctx)

		# print before invoke
		self.before_invoke(self.before_command)

		self.logger.info('Finished init...')

	async def update_status(self):
		srv = len(self.guilds)

		usr = 0
		for guild in self.guilds:
			usr += len(guild.members)

		await self.change_presence(activity=discord.Game(name=f'.help | {srv} guild{"s" if srv > 1 else ""} | {usr} user{"s" if usr > 1 else ""}'))

	async def request(self, method, url, **args):
		self.logger.info(f"{method.upper()} request url: '{url}' args: {saferepr(args)}")
		try:
			async with self.session.request(method, url, **args) as resp:
				if resp.status != 200:
					return None
				if resp.content_type == 'application/json':
					return await resp.json(), resp.content_type
				elif resp.content_type.startswith('image'):
					return await resp.read(), resp.content_type
				elif resp.content_type.startswith('text'):
					return await resp.text(), resp.content_type
				else:
					return None
		except:
			return None

	async def before_command(self, ctx):
		uname = ctx.author.name
		sname = ctx.guild.name
		uid = ctx.author.id
		sid = ctx.guild.id
		mid = ctx.message.id
		cmd = ctx.command.name

		if ctx.invoked_subcommand is not None:
			cmd = ctx.command.name if ctx.invoked_subcommand is None else ctx.invoked_subcommand

		argstr = ''
		if len(ctx.args) > 2:
			argstr += f' args={saferepr(ctx.args[2:])}'
		if ctx.kwargs:
			argstr += f' kwargs={saferepr(ctx.kwargs)}'

		self.logger.info(f'cmd={cmd} usr={uid} ({uname}) srv={sid} ({sname}) msg={mid}{argstr}')

	async def blacklist_ctx(self, ctx):
		return not self.blacklist(ctx.message)

	def blacklist(self, message):
		return message.author.id in self.ignore_users or message.author.bot or not isinstance(message.channel, discord.TextChannel)

	async def on_member_join(self, member):
		await self.update_status()

	async def on_member_remove(self, member):
		await self.update_status()

	async def on_guild_join(self, guild):
		await self.update_status()

	async def on_guild_remove(self, guild):
		await self.update_status()

	async def on_ready(self):
		self.logger.info('Setting up user and extensions...')

		if not hasattr(self, 'startup_time'):
			self.startup_time = datetime.now()

		await self.user.edit(username=self.config['nick'])
		await self.update_status()

		for extension in extensions:
			self.logger.debug(f'Loading extension: {extension}')
			self.load_extension(extension)

		self.logger.info(f'Logged in as: {self.user.name} ({self.user.id}), discord.py version {discord.__version__}')
		self.logger.info(f'Connected to {len(self.guilds)} servers')

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			return

		#self.logger.warning(f'Command error: ', exc_info=)

		errors = {
			commands.DisabledCommand: 'Command has been disabled.',
			commands.MissingPermissions: 'Invoker is missing permissions to run this command.',
			commands.BotMissingPermissions: 'Bot is missing permissions to run this command.',
			commands.CommandOnCooldown: 'Please wait before running command again.',
		}

		for type, text in errors.items():
			if isinstance(error, type):
				return await ctx.send(errors[type])

		# argument error
		if isinstance(error, commands.UserInputError):
			return await ctx.send(f'Invalid argument(s) provided.\n```{ctx.command.signature}```')

		# await ctx.send(f'An error occured in `{ctx.command.name}` invoked by {ctx.message.author}:\n```{error}```')
		if hasattr(error, 'original'):
			self.logger.error(error.original)
			raise error.original


# overwrite discord.Embed with a monkey patched class that automatically sets the color attribute
class Embed(discord.Embed):
	def __init__(self, color=0x4A5E8C, **attrs):
		attrs['color'] = color
		super().__init__(**attrs)


discord.Embed = Embed

if __name__ == '__main__':
	bot = AceBot()
	bot.run(bot.config['token'])
