import discord
import re
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='`')

unicodeEmojis = open("emoji_unicode.txt","r",encoding="utf16")
lines = unicodeEmojis.readlines()
emojiList = []
for line in lines:
    emojiIndex = line.index("(") + 1
    emojiList.append(line[emojiIndex])

@client.event
async def on_message(message):
#    server = message.server
#    global_emojis = server.emojis

    splitMessage = re.split('[ :\n]',str(message.content))
    delete = True
    
    print(splitMessage)

    
#==============================================================================
#     OUTLINE:
#     1. Convert the message to something we can interpret
#         1. Cases:
#             1. The message is all emoji objects (strip empty space characters)
#             2. The message is all unicode emotes
#             3. The message is a mix of the two
#             4. The message contains something that is not an emote
#             5. The message is an image.
#==============================================================================

    index = 0
    for part in splitMessage:     
        checkOneIndexBackward = splitMessage[index - 1]
        
        #case 1: the part is an unicode emoji
        if(part in emojiList):
            delete = False
        
        #case 2: the part is an emote object
        elif(part == '<' and len(part) == 1):
            delete = False
        
        #case 2.5: if there is no spaces between the emote objects
        elif(part == '<' and len(part) == 1 and len(splitMessage[index + 2]) == 20):
            try:
                checkTwoIndexForward = splitMessage[index + 2]
                if(checkTwoIndexForward[-1] == '<'):
                    delete = False
            except IndexError:
                delete = False
        
        #case 3: the part is the numbers and the '>' of the emote object
        elif(len(part) == 19 and part[-1] == '>'):
            delete = False
        
        #case 4: if theres no spaces between the emote objects
        elif(len(part) == 20 and part[-1] == '<'):
            delete = False
        
        #case 5: the part is just a space
        elif(not part):
            delete = False
            
        #case 6: the part is the name of the global emote object
        elif(checkOneIndexBackward[-1] == '<'):
            delete = False
            
        else:
            delete = True
            break
        
        index += 1
    
    if(splitMessage==['']):
        delete = True
    
    if delete:
        await client.delete_message(message)

    # await client.delete_message(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('MzQ3MjE5NjM0MjQ1ODYxMzg2.DMUWwA.MIQ_k6nhwnJO7PpohV4PnetlyzE')
