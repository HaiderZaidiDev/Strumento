import discord # Imports discord module. 
import urllib.request # Imports urllib.request module
import os # Imports os module. 
import json

client = discord.Client() # Creates discord client. 

@client.event # Defining client event. 
async def on_ready(): # Defines event response. (Executes on successful join). 
  serverCount = len(client.servers) # Counts the number of servers the bot is currently in. 
  print(str(client.user) + ' is now online and is being used in ' + str(serverCount) + ' server(s):') # Prints success message.
  print() # Prints blank message.

  for joinedServers in client.servers: # For loop to access list of servers the bot is currently in.
    print(joinedServers) # Prints all the servers the bot is currently in. 
   
  

@client.event # Defining client event. 
async def on_message(message): # Defines event response. (Executes on message.)
    if message.author != client.user: # If the message isn't sent by the bot, the following code is executed. 
    
      if message.content.startswith('+ping'):
        await client.send_message(message.channel, 'Pong!')


      if message.content.startswith('+screenshot'): # If the users message starts with +screenshot the following code is executed.

        inspectUrl = message.content.replace('+screenshot ','') # Removes +screenshot and the following space from the users message, assigns it to a variable.
        screenShot = "https://csgo.gallery/" + inspectUrl # Appends inspect url to csgo.gallery link. 


        screenShotOld = urllib.request.Request(screenShot, headers={'User-Agent': 'Mozilla/5.0'}) # Requests url of the appending link with user agent as Mozilla. This is done to avoid 403 errors when getting the final redirect link.

        screenShotRedir = urllib.request.urlopen(screenShotOld).geturl() # Assigns the final redirect link to variable screenShotRedir

        if screenShotRedir == str('https://cs.deals/'): # If the final redirect returns back to the cs.deals homepage, meaning the inspect url was incorrect, the following code is executed. 
            await client.send_message(message.channel, 'An invalid inspect url was provided, please try again.') # Prints message to user stating inspect url was invalid. 

        else: # If the inspect url is valid, the following code is executed:
          knifeID = [500, 505,506, 507, 508, 509, 512, 514, 515, 516, 519, 520, 522, 523]
          for apiData in urllib.request.urlopen('https://api.csgofloat.com/?url=' + inspectUrl): # Opens API for CS:GO Skins. 
            jsonToPython = json.loads(apiData.decode('utf-8')) # Loads json from apiData.



            weapon_type = jsonToPython['iteminfo']['weapon_type'] # Weapon name.
            skin_name = jsonToPython['iteminfo']['item_name'] # Skin Name.

            skin = '**Skin: **' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
            raw_skin = weapon_type + ' %7C ' + skin_name
            statSkin = '**Skin: **StatTrak™ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
            statSkin_raw = 'StatTrak%E2%84%A2 ' + weapon_type + ' %7C ' + skin_name

            if jsonToPython['iteminfo']['defindex'] in knifeID:
              print('is knife')
              skin = '**Skin: **★ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
              raw_skin = '%E2%98%85 ' + weapon_type + ' %7C ' + skin_name
              statSkin = '**Skin: **★ StatTrak™ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
              statSkin_raw = '%E2%98%85 StatTrak%E2%84%A2 ' + weapon_type + ' %7C ' + skin_name

            #gold = 'gold'
            #test = jsonToPython['iteminfo']['stickers'][0]

            print(len(jsonToPython['iteminfo']['stickers']))

            # Checks if the skin is souvenier (if the first sticker has the word gold in it)
            if len(jsonToPython['iteminfo']['stickers']) > 0:
              if jsonToPython['iteminfo']['origin'] == 8 and str('gold') in jsonToPython['iteminfo']['stickers'][0]['codename'] :
                skin = '**Skin: ** Souvenir ' + weapon_type + ' | ' + skin_name
                raw_skin = 'Souvenir ' + weapon_type + ' %7C ' + skin_name
                
            else: 
              print('no')

            statByte = statSkin_raw.encode('utf-8')
            StrFloatValue = str(jsonToPython['iteminfo']['floatvalue']) # Float value as string. 
            skin_floatValue = '**Float: **'  + StrFloatValue # Float value with suffix. 

            raw_floatValue = jsonToPython['iteminfo']['floatvalue'] # Float value as float. 

          #-- Determines wear of the skin based upon the float value. 

            if raw_floatValue < 0.07: # If the flow is below 0.07 the follopw
              wear = 'Factory New'
            
            if raw_floatValue > 0.07 and raw_floatValue < 0.15:
              wear = 'Minimal Wear'

            if raw_floatValue > 0.15 and raw_floatValue < 0.37:
              wear = 'Field-Tested'

            if raw_floatValue > 0.37 and raw_floatValue < 0.44:
              wear = 'Well-Worn'

            if raw_floatValue > 0.44:
              wear = 'Battle-Scarred'
            

            marketWear = ' %28' + wear + '%29'
            wearHash = '(' + wear + ')'
            suffixWear = '**Wear: **' + wear
            marketHash = weapon_type + ' | ' + skin_name + ' ' + wearHash
            print(marketHash)


            #------- STICKER DETECTION
            if len(jsonToPython['iteminfo']['stickers']) == 4:
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']
              wearThree = jsonToPython['iteminfo']['stickers'][2]['wear']
              wearFour = jsonToPython['iteminfo']['stickers'][3]['wear']
            
            if len(jsonToPython['iteminfo']['stickers']) == 3:
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']
              wearThree = jsonToPython['iteminfo']['stickers'][2]['wear']

            if len(jsonToPython['iteminfo']['stickers']) == 2:
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']

            if len(jsonToPython['iteminfo']['stickers']) == 1:
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']

            if len(jsonToPython['iteminfo']['stickers']) == 0:
              stickerOutput =  ''

            
            else:
              if len(jsonToPython['iteminfo']['stickers']) == 4:
                if wearOne == None:
                  wearOne = 0
                else:
                  wearOne = wearOne*100

                if wearTwo == None:
                  wearTwo = 0
                else:
                  wearTwo = wearTwo*100

                if wearThree == None:
                  wearThree = 0
                else:
                  wearThree = wearThree*100

                if wearFour == None:
                  wearFour = 0
                else:
                  wearFour = wearFour*100
              
              if len(jsonToPython['iteminfo']['stickers']) == 3:
                if wearOne == None:
                  wearOne = 0
                else:
                  wearOne = wearOne*100

                if wearTwo == None:
                  wearTwo = 0
                else:
                  wearTwo = wearTwo*100

                if wearThree == None:
                  wearThree = 0
                else:
                  wearThree = wearThree*100

              if len(jsonToPython['iteminfo']['stickers']) == 2:
                if wearOne == None:
                  wearOne = 0
                else:
                  wearOne = wearOne*100

                if wearTwo == None:
                  wearTwo = 0
                else:
                  wearTwo = wearTwo*100

              if len(jsonToPython['iteminfo']['stickers']) == 1:
                if wearOne == None:
                  wearOne = 0
                else:
                  wearOne = wearOne*100

              
              if len(jsonToPython['iteminfo']['stickers']) == 4:
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerThree = '(' + str(wearThree)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][2]['name']
                stickerFour = '(' + str(wearFour)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][3]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo + '\n' + stickerThree + '\n' + stickerFour

              if len(jsonToPython['iteminfo']['stickers']) == 3:
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerThree = '(' + str(wearThree)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][2]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo + '\n' + stickerThree

              if len(jsonToPython['iteminfo']['stickers']) == 2:
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo 
              
              if len(jsonToPython['iteminfo']['stickers']) == 1:
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne 
              





            if jsonToPython['iteminfo']['killeaterscoretype'] == None:
              rawMarketSkin = raw_skin + marketWear
            
            else:
              rawMarketSkin = statSkin_raw + marketWear


            marketSkinOutput = rawMarketSkin.replace(' ', '+')
            patternIndex = '**Index: **' + str(jsonToPython['iteminfo']['paintseed']) # Pattern index with suffix. 
            
            print(marketSkinOutput)

            price = 'https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=' + marketSkinOutput

            print(price)
            

            for priceAPIData in urllib.request.urlopen(price):
              jsonToPython = json.loads(priceAPIData.decode('utf-8'))

              if str('median_price') not in jsonToPython:
                marketMedianOutput = '**Avg. Price:** *Not available.*'
              
              else: 
                marketMedian = jsonToPython['median_price'] # Opens API for CS:GO Skins. 
                marketMedianOutput = '**Avg. Price:** ' + marketMedian
            

            marketLink = 'https://steamcommunity.com/market/search?appid=730&q=' + marketSkinOutput
            marketLinkOutput = '**Market: **[[Link]]' + '(' + marketLink + ')'
            

            bitskinsLink = 'https://bitskins.com/?market_hash_name=' + marketSkinOutput + '&appid=730'
            bitskinsLinkOutput = '**Bitskins: **[[Link]]' + '(' + bitskinsLink + ')' 
            for apiData in urllib.request.urlopen('https://api.csgofloat.com/?url=' + inspectUrl): # Opens API for CS:GO Skins. 
              jsonToPython = json.loads(apiData) # Loads json from apiData.

            if jsonToPython['iteminfo']['defindex'] in knifeID:
              msgOutput = '__**Information:**__ \n' + skin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput  

              msgOutputStat = '__**Information:**__ \n' + statSkin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput 
            
            else:
              msgOutput = '__**Information:**__ \n' + skin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput + '\n' + stickerOutput 

              msgOutputStat = '__**Information:**__ \n' + statSkin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput + '\n' + stickerOutput




            print(marketSkinOutput)



            for apiData in urllib.request.urlopen('https://api.csgofloat.com/?url=' + inspectUrl):
              jsonToPython = json.loads(apiData.decode('utf-8')) # Loads json from apiData.

            if jsonToPython['iteminfo']['killeaterscoretype'] == None:
              emb = discord.Embed(description= msgOutput, colour = 0x00b2ff) # Outputs data of the skin fetched from the inspect url. 
              emb.set_image(url=screenShotRedir) # Sets the embed as an image; screenShotRedir
              await client.send_message(message.channel, embed=emb) # Prints the embe
            
            else: 
              emb = discord.Embed(description= msgOutputStat , colour = 0x00b2ff) # Outputs data of the skin fetched from the inspect url. 
              emb.set_image(url=screenShotRedir) # Sets the embed as an image; screenShotRedir
              await client.send_message(message.channel, embed=emb) # Prints the embed.

token = os.environ.get("DISCORD_BOT_SECRET") # Assigning secret token. 
client.run('NTI3MjU0OTY0MjU1MzI2MjI4.DwREYQ.Bo2ncCt3BYFA3e-GmNxtNLZaFMA') # Verifying secret token. 
