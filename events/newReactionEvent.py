from src.functions import createEmbed, newLog
import shelve, sys


def setNewReactionEvent(self):
    @self.client.event
    async def on_raw_reaction_add(payload):
        if payload.user_id == self.config['usersIDs'].getint('botId'):
            return
        await fillEmoji(self, payload)

def checkNewNotification(self, messageId, userId):
    users = self.db.getValue(tableName = 'shedule', argument = 'users', selector = 'messageId', value = messageId)
    users = eval(users)
    if userId not in users:
        users.append(userId)
        self.db.update(tableName = 'shedule', argument = 'users', selector = 'messageId', newValue = users, findValue = messageId)

async def giveRequestsRole(self, messageId, userId):
    if str(messageId) == self.config['requestsData']['getRoleMessage']:
        guild = await self.client.fetch_guild(self.config['data']['guildId'])
        role = guild.get_role(int(self.config['requestsData']['roleID']))
        user = await guild.fetch_member(userId)
        await user.add_roles(role)

async def pickColor(self, messageId, userId, emoji):

    colors = {667431391918555174: 858131191999758337,
                667431417973702666: 858131223175888926,
                667431463024590894: 858131253634007050,
                667431510307241984: 858131332597415936,
                667431579530035200: 858131352599527435,
                667431676627910687: 858131393602125834,
                667431704868290578: 858131403358208030,
                667431741736353803: 858131411244417024,
                667431773659201578: 858131428705566720,
                667431996104114198: 858131438796537876,
                667432024604409869: 858131449046499328,
                667432051896483842: 858131461940314142,
                667432082603114497: 858131473504403466,
                667432127893209098: 858131493549637663,}
    if messageId == 858131920729931796:
        if emoji.id in colors.keys():
            guild = await self.client.fetch_guild(self.config['data']['guildId'])
            role = guild.get_role(colors[emoji.id])
            user = await guild.fetch_member(userId)
            await user.add_roles(role)


async def fillEmoji(self, payload):
    messageId = payload.message_id
    userId = payload.user_id
    emoji = payload.emoji
    channelId = payload.channel_id

    colorRoles = [667431391918555174,
                    667431417973702666,
                    667431463024590894,
                    667431510307241984,
                    667431579530035200,
                    667431676627910687,
                    667431704868290578,
                    667431741736353803,
                    667431773659201578,
                    667431996104114198,
                    667432024604409869,
                    667432051896483842,
                    667432082603114497,
                    667432127893209098]

    sheduleEmoji = self.client.get_emoji(810182035955777576)


    if sheduleEmoji == emoji and str(channelId) == self.config['sheduleData']['sheduleChannel']:
        checkNewNotification(self, messageId, userId)
        return

    if '⛏️' ==  str(emoji) and str(channelId) == self.config['requestsData']['getRoleChannel']:
        await giveRequestsRole(self, messageId, userId)
        return

    if emoji.id in colorRoles:
        await pickColor(self, messageId, userId, emoji)
        return

    if emoji.id == 872127853230174308 and messageId == 877522157498929243:
        guild = await self.client.fetch_guild(self.config['data']['guildId'])
        role = guild.get_role(877522465889353738)
        user = await guild.fetch_member(userId)
        await user.add_roles(role)
        return


    try:
        if channelId != self.config['requestsData'].getint('channel'):
            return
        accessEmoji = {'2️⃣': 2, '3️⃣': 3, '4️⃣': 4}
        channel = self.client.get_channel(channelId)
        msg = await channel.fetch_message(messageId)
        try:
            embed = msg.embeds[0].to_dict()
        except:
            return



        msgIds = self.db.getValue(tableName = 'requestsData', argument = 'requests_ids', selector = 'user_id', value = userId)
        emojiIds = self.db.getValue(tableName = 'emojiData', argument = 'helper_ids', selector = 'request_id', value = messageId)


        # проверка на существование заявки
        if emojiIds:
            timeEmoji = eval(emojiIds)
        else:
            return

        # проверка на эмодзи + создателя заявки
        if '🔒' == str(emoji):
            if msgIds:
                msgIds = eval(msgIds)
                if messageId in msgIds:
                    guild = await self.client.fetch_guild(payload.guild_id)
                    user = await guild.fetch_member(userId)
                    newEmbed = createEmbed(description = '~~' + embed['description'] + '~~', thumbnail = embed['thumbnail']['url'], footer = embed['footer']['text'],
                                            authorName = '{0} закрыл заявку.'.format(user.display_name), authorIconURL = embed['author']['icon_url'], color = embed['color'])
                    await msg.edit(content = None, embed = newEmbed)
                    await msg.unpin()

                    msgIds.remove(messageId)
                    if len(msgIds) == 0:
                        self.db.remove(tableName = 'requestsData', selector = 'user_id', value = userId)
                    else:
                        self.db.update(tableName = 'requestsData', argument = 'requests_ids', selector = 'user_id', newValue = str(msgIds), findValue = userId)

                    self.db.remove(tableName = 'emojiData', selector = 'request_id', value = messageId)
                    return

            if userId != self.config['usersIDs']['botId']:
                await msg.remove_reaction(emoji = emoji, member = payload.member)
            return


        # Проверка на любой эмоджи от создателя заявки
        if msgIds:
            msgIds = eval(msgIds)

            if messageId in msgIds:
                await msg.remove_reaction(emoji = payload.emoji, member = payload.member)
                return

        # Проверка на доступные эмодзи от любого другого пользователя кроме создателя заявки
        if str(emoji) in accessEmoji.keys():
            timeEmoji = await addReaction(self, accessEmoji[str(emoji)], timeEmoji, msg, payload, embed)

            if timeEmoji:
                self.db.update(tableName = 'emojiData', argument = 'helper_ids', selector = 'request_id', newValue = str(timeEmoji), findValue = messageId)
            return


        # Очистка эмодзи если заявка есть, но эмодзи не доступен
        if str(emoji) not in accessEmoji.keys():
            await msg.remove_reaction(emoji = payload.emoji, member = payload.member)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        newLog(exc_type, exc_obj, exc_tb, e)




async def addReaction(self, id, timeEmoji, msg, payload, embed):
    if id not in timeEmoji.keys():
        if payload.user_id in timeEmoji.values() and payload.user_id != self.config['usersIDs']['botId']:
            await msg.remove_reaction(emoji = payload.emoji, member = payload.member)
            return 0
        else:
            timeEmoji[id] = payload.user_id
            await addInEmbed(id, msg, payload, embed)
    else:
        if payload.user_id != self.config['usersIDs']['botId']:
            await msg.remove_reaction(emoji = payload.emoji, member = payload.member)
            return 0

    return timeEmoji

async def addInEmbed(id, msg, payload, embed):
    newUser = '***{0}) Слот:** <@{1}>*'.format(id, payload.user_id)
    splitEmbed = embed['description'].split('\n')
    splitEmbed[3 + id] = newUser
    newEmbed = createEmbed(description = '\n'.join(splitEmbed), thumbnail = embed['thumbnail']['url'], footer = embed['footer']['text'],
                            authorName = embed['author']['name'], authorIconURL = embed['author']['icon_url'], color = embed['color'])
    await msg.edit(embed = newEmbed)
