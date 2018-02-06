#!/usr/bin/env python3
# encoding: utf-8

import json
import sys
import traceback

import aiohttp
from discord.ext import commands

"""A simple stats cog, for use with several bot lists.
Make sure your bot.config['tokens']['stats'] has a key
which maps each domain name to either null or a token.
"""


class StatsAPI:
	# credit to @Tom™#7887 (ID 248294452307689473) on the Discord Bots List guild
	# for much of this
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)
		self.config = self.bot.config['tokens']['stats']

	def __unload(self):
		self.bot.loop.create_task(self.session.close())

	async def send(self, url, headers={}, data={}):
		"""send the statistics to the API gateway."""
		async with self.session.post(url, data=data, headers=headers) as resp:
			print('[STATS]', self.config_section, end=' ', file=sys.stderr)
			if resp.status // 100 == 2:  # 2xx codes are success
				print('response:', await resp.text(), file=sys.stderr)
			else:
				print('failed with status code', resp.status, file=sys.stderr)

	@property
	def api_key(self):
		return self.config[self.config_section]

	@property
	def guild_count(self):
		return len(self.bot.guilds)

	@commands.command(name='stats', hidden=True)
	@commands.is_owner()
	async def send_command(self, context):
		try:
			await self.send()
		except:
			response = '\N{cross mark}'
			print(traceback.format_exc(), file=sys.stderr)
		else:
			response = '\N{white heavy check mark}'
		await context.message.add_reaction(response)

	async def on_ready(self):
		await self.send()

	async def on_guild_join(self, server):
		await self.send()

	async def on_guild_remove(self, server):
		await self.send()


class DiscordPWStats(StatsAPI):
	config_section = 'bots.discord.pw'

	async def send(self):
		await super().send(
			'https://bots.discord.pw/api/bots/%s/stats' % self.bot.user.id,
			data=json.dumps({'server_count': self.guild_count}),
			headers={
				'Authorization': self.api_key,
				'Content-Type': 'application/json'})


class DiscordBotList(StatsAPI):
	config_section = 'discordbots.org'

	async def send(self):
		await super().send(
			'https://discordbots.org/api/bots/%s/stats' % self.bot.user.id,
			data=json.dumps({'server_count': self.guild_count}),
			headers={
				'Authorization': self.api_key,
				'Content-Type': 'application/json'})


class Discordlist(StatsAPI):
	config_section = 'bots.discordlist.net'

	async def send(self):
		await super().send(
			'https://bots.discordlist.net/api',
			data=json.dumps({
				'token': self.api_key,
				'servers': self.guild_count}),
			headers={'Content-Type': 'application/json'})


def setup(bot):
	for Cog in (DiscordPWStats, DiscordBotList, Discordlist):
		stats_config = bot.config['tokens']['stats']
		if stats_config.get(Cog.config_section) is not None:
			bot.add_cog(Cog(bot))
		else:
			print(Cog.config_section, "was not loaded! Please make sure it's configured properly.")
