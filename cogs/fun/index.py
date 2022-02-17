import discord
import random
from discord.ext import commands
from bin.converters import *
from bin.functions import get_embed

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        description = 'Проверка пинга',
        aliases = ['пинг'],
        brief='Проверка пинга'
    )
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(ctx.bot.latency * 1000)} ms')

    @commands.command(
        name = 'check',
        aliases = ['чек'],
        description = 'Поиск юзера',
        brief='Узнать когда юзер зашёл',
        usage = '<имя пользователя>|<ID>'
    )
    async def joined(self, ctx, *, member: UserConverter = None):
        member = member or ctx.author
        time = member.joined_at.strftime("%m/%d/%Y, %H:%M")
        req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
        banner_url = ''
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
        await ctx.send(f'{member} joined on {time}\n{member.avatar}\n{banner_url}')

    @joined.error
    async def joined_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

    @commands.command(
        aliases=['число'],
        usage='<from>-<to>',
        description='Роллим гачу <:ad:812513742000619520>',
        brief='Рандом число <от>-<до>'
    )
    async def roll(self, ctx, *, args = None):
        if args is None:
            #raise commands.BadArgument
            return await ctx.send_help('roll')

        args = args.split('-')
        if len(args) != 2 or not args[0].isdigit() or not args[1].isdigit():
            raise commands.BadArgument

        try:
            number = random.randint(int(args[0]), int(args[1]))
        except ValueError:
            raise commands.BadArgument
        await ctx.send(f'Yours roll is {number}')

    @roll.error
    async def joined_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('<:MonkaStop:837405113638977576>')



    @commands.command(name = 'вебивент', aliases = ['веб', 'ивент'])
    async def web_event_link(self, ctx):
        return await ctx.send('<https://webstatic-sea.mihoyo.com/ys/event/e20220128lantern/index.html>\n<https://webstatic-sea.mihoyo.com/ys/event/e20220129-postcard/index.html>')

    @commands.command(name = 'примогемы')
    async def primogems_link(self, ctx):
        return await ctx.send('<https://docs.google.com/spreadsheets/d/1DPJOtHTLB_y-MTcUheSBrMPFvV_EtBlcYA6Xy1F0R_c/edit?pli=1#gid=284498967>')

    @commands.command(name = 'форум', aliases = ['forum'])
    async def forum_link(self, ctx):
        return await ctx.send('Ссылка на форум - <https://www.hoyolab.com>\nСсылка на логин бонус - <https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=ru-ru>')

    @commands.command(name = 'карта', aliases = ['map'])
    async def map_link(self, ctx):
        return await ctx.send('Интерактивная карта по Геншину: <https://webstatic-sea.mihoyo.com/app/ys-map-sea/?lang=ru-ru>')

    @commands.command(name = 'хх', aliases = ['hh'])
    async def hh_link(self, ctx):
        return await ctx.send('<https://genshin.honeyhunterworld.com>')

    @commands.command(name = 'паймон')
    async def paimon_link(self, ctx):
        return await ctx.send('https://paimon.moe/')

    @commands.command(name = 'яишенка', aliases = ['глазунья'])
    async def jaishenka(self, ctx):
        answer = ('<a:read:859186021488525323> Ставишь сковороду на небольшую температуру, наливаешь немного масла, растираешь силиконовой кисточкой или салфеткой равномерно, чтобы не хлюпало, разбиваешь яйцо и ждёшь\n\n' +
                    '<a:read:859186021488525323> Видишь, что нижний слой белка начинает белеть, а сверху вокруг желтка еще сопелька прозрачная, так вот, бери вилочку и под сопелькой в радиусе разлива яйца разрывай белок, чтобы слой вокруг желтка тип провалился к сковородке и стал одним целым со всем белком, посыпаешь приправами на вкус, ждешь, огонь сильно не добавляешь и готово\n\n' +
                    '<a:peepoFAT:859363980228427776> Если любишь, чтобы желток внутри приготовился и был не жидкий, то накрываешь крышкой')
        return await ctx.send(answer)


    @commands.command(aliases = ['арольф', 'арофл'])
    async def arolf(self, ctx):
        arolf_file = discord.File('files/photo/aRolf.png')
        return await ctx.send(file = arolf_file)

    @commands.command(aliases = ['токсины'])
    async def toxic(self, ctx):
        return await ctx.send(f'Уровень токсинов в чате {random.randint(1, 100)}% <:peepoSitStarege:933802101824430201>')

    @commands.command(aliases = ['ссылочки', 'круточки'])
    async def link(self, ctx):
        return await ctx.send('Запись стримов и круточек - <https://www.twitch.tv/yoko_o0>\nВесь материальчик по кадровому <https://www.youtube.com/channel/UCgis0wZn_m5mFNQHzvqyf8w>')

    @commands.command(aliases = ['база'])
    async def base_message(self, ctx, message_link=None):
        channel = await ctx.bot.fetch_channel(942169382124134410)
        if ctx.message.attachments:
            files = None
            file_ = None
            if len(ctx.message.attachments) > 1:
                files = []
                for file in ctx.message.attachments:
                    file = await file.to_file()
                    files.append(file)
            else:
                file_ = await ctx.message.attachments[0].to_file()
            await channel.send(content=f'База от {ctx.message.author.mention}',
                               files=files,
                               file=file_
                               )
            await ctx.send('Добавила базу <:BASEDHM:897821614312394793>')
            return None
        try:
            message_id = message_link.split('/')[6]
            channel_id = message_link.split('/')[5]
            mes_channel = await ctx.bot.fetch_channel(channel_id)
            message = await mes_channel.fetch_message(message_id)
        except:
            return await ctx.send('Не нашла базу(')
        files = None
        file_ = None
        if message.attachments:
            if len(message.attachments) > 1:
                files = []
                for file in message.attachments:
                    file = await file.to_file()
                    files.append(file)
            else:
                file_ = await message.attachments[0].to_file()
        await channel.send(content=f'База от {message.author.mention}\n{message.content}',
                           files=files,
                           file=file_,
                           embeds=message.embeds,
                           )
        await ctx.send('Добавила базу <:BASEDHM:897821614312394793>')
    #@commands.command()
    #async def test(self, ctx, user: discord.Member, role: discord.Role):
    #    return await user.add_roles(role)






def setup(bot):
    bot.add_cog(Fun(bot))
