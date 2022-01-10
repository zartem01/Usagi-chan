import discord
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config


    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit = limit + 1)
        await ctx.send('Успешно удалила', delete_after = 10)

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, channel_id: int, *, message: str):
        try:
            channel = await ctx.bot.fetch_channel(channel_id)
        except:
            guild = await ctx.bot.fetch_guild(self.config['data']['guild_id'])
            channel = guild.get_thread(channel_id)
        await channel.send(message)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Nothing to see here comrade.')
        else:
            print(error)

    @commands.command()
    @commands.is_owner()
    async def connect(self, ctx, channel_id: int):
        channel = await ctx.bot.fetch_channel(channel_id)
        await channel.connect()
        await ctx.send('Успешно подключилась')

    @connect.error
    async def connect_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Nothing to see here comrade.')
        else:
            print(error)


    @commands.command(name = 'помощь', aliases = ['хелп', 'хлеп'])
    async def help(self, ctx, *, args = None):
        if args:
            await ctx.send_help(args)
        else:
            await ctx.send_help()

    @commands.command(name = 'redirect')
    @commands.is_owner()
    async def redirect(self, ctx, switch: str):
        if switch == 'on':
            self.bot.redirection = True
            answer = 'Включила переадресацию'
        elif switch == 'off':
            self.bot.redirection = False
            answer = 'Выключила переадресацию'
        await ctx.send(answer)






def setup(bot):
    bot.add_cog(Main(bot))
