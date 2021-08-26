import discord
import random
from discord.ext import commands
from bin.functions import UserConverter

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = 'Проверка пинга', aliases = ['пинг'], brief='Проверка пинга')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(ctx.bot.latency * 1000)} ms')

    @commands.command(name = 'check', aliases = ['чек'], description = 'Поиск юзера', brief='Узнать когда юзер зашёл')
    async def joined(self, ctx, *, member: UserConverter = None):
        member = member or ctx.author
        time = member.joined_at.strftime("%m/%d/%Y, %H:%M")
        await ctx.send('{0} joined on {1}'.format(member, time))

    @joined.error
    async def joined_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

    @commands.command(aliases=['число'], usage='<from>-<to>', description='Роллим гачу :AD:', brief='Рандом число <от>-<до>')
    async def roll(self, ctx, *, args):
        args = args.split('-')
        if len(args) != 2 or not args[0].isdigit() or not args[1].isdigit():
            raise commands.BadArgument
        await ctx.send(f'Yours roll is {random.randint(int(args[0]), int(args[1]))}')

    @roll.error
    async def joined_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Wrong argumets')


    @commands.group()
    async def first(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("This is the first command layer")

    @first.group()
    async def second(self, ctx):
        print(ctx.invoked_subcommand)
        if ctx.invoked_subcommand is None:
            await ctx.message.author.send("Hey! Did this come through clearly?")

    @second.command()
    async def third(self, ctx, channelId=None):
        if channelId != None:
            channel = self.bot.get_channel(int(channelId))
            await channel.send("Hey! This is a message from me the bot. Bet you didn't see who ran the command?", delete_after=15)




def setup(bot):
    bot.add_cog(Fun(bot))
