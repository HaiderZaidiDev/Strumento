import discord # Imports discord module. 
import urllib.request # Imports urllib.request module
import os # Imports os module. 
import json # Imports Json Module
import sys

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
    
      if message.content.startswith('+ping'): # If the user enters +ping, the following code is executed.
        await client.send_message(message.channel, 'Pong!')
      
      if message.content.startswith('+info'): # If the user enters +info, the following code is executed. 
        infoMessage = '''
        __**Information**__:
        
        This bot was made by Nitr0us#5090, if you have any questions or require support please contact him.
        
        __**Commands**__:
        
        **1)** Screenshot:
        Usage: +screenshot <inspecturl> 
        Purpose: Displays an informative screenshot of your CS:GO item, along with various pricing/listing information.
        
        Note: This may take a few seconds to generate. 
        
        **2)** Ping:
        Usage: +ping
        Purpose: To test if the bot is online, and behaving correctly. 
        
        Note: If this doesn't result in the bot sending a message, contact the bot developer. 
        
        **3)** Donate:
        Usage: +donate
        Purpose: Provides the bot developers paypal.me link. 
        
        Note: Hosting a Discord bot does cost a bit of money, all donations will go towards hosting bots.
        
        __**Sources:**__:
        
        **1)** [CSGOFloat](https://csgofloat.com/)
        Type: API 
        Use:  Used to determine all information provided under the 'Information:' section of the screenshot. 
        
        ** 2)** [Steam](https://store.steampowered.com/)
        Type: API
        Use: Used to determine the average prices of skins. 
        
        ** 3)** [CSGO.Gallery](https://cs.deals/)
        Type: URL
        Use: Generated screenshots. 
        '''
        emb = discord.Embed(description=infoMessage, colour= 0x00b2ff)
        await client.send_message(message.channel, embed=emb)


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
            raw_skin = weapon_type + ' %7C ' + skin_name # Skin string with percent encoding. 
            statSkin = '**Skin: **StatTrak™ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
            statSkin_raw = 'StatTrak%E2%84%A2 ' + weapon_type + ' %7C ' + skin_name # Stat trak skin string with percent encoding. 

            if jsonToPython['iteminfo']['defindex'] in knifeID: # If the skin is a knife, the followeing code is executed.
              skin = '**Skin: **★ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
              raw_skin = '%E2%98%85 ' + weapon_type + ' %7C ' + skin_name # Skin string with percent encoding. 
              statSkin = '**Skin: **★ StatTrak™ ' + weapon_type + ' | ' + skin_name # Weapon + Skin Name
              statSkin_raw = '%E2%98%85 StatTrak%E2%84%A2 ' + weapon_type + ' %7C ' + skin_name # Stat trak skin string with percent encoding


            if len(jsonToPython['iteminfo']['stickers']) > 0: # If the skin has a sticker, the following code is executed.
              #--- Souvenier Detection
              #- NOTE: This may give false positives/not always work accurately, i.e if a gold sticker was put on a unboxed skin, or stickers were removed from a souvenier skin this would not detect that. 
              #        Always look at the screenshot to determine if the skin is souvenier or not for 100% accuracy. 
              if jsonToPython['iteminfo']['origin'] == 8 and str('gold') in jsonToPython['iteminfo']['stickers'][0]['codename']: # If the skin was unboxed, and has a sticker with the word gold in it the following code is executed.
                skin = '**Skin: ** Souvenir ' + weapon_type + ' | ' + skin_name # Adds souvenier suffix to skin.
                raw_skin = 'Souvenir ' + weapon_type + ' %7C ' + skin_name # Adds souvenier suffix to skin name with percent encoding.
            
            
            StrFloatValue = str(jsonToPython['iteminfo']['floatvalue']) # Float value as string. 
            skin_floatValue = '**Float: **'  + StrFloatValue[0:11] # Float value with suffix, used in embed. 
            
            #--- Wear detection
            #- Determines wear of the skin based upon the float value. 

            raw_floatValue = jsonToPython['iteminfo']['floatvalue'] # Float value as float. 

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
            

            
            marketWear = ' %28' + wear + '%29' # Adds brackets via percent encoding around the wear of the skin.
            wearHash = '(' + wear + ')' # Adds brackets around the wear of the skin.
            suffixWear = '**Wear: **' + wear # Wear output to be displayed in the embed (wear with suffix).



            #------- STICKER DETECTION
            if len(jsonToPython['iteminfo']['stickers']) == 4: # If there are 4 stickers, the following code is executed.
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']
              wearThree = jsonToPython['iteminfo']['stickers'][2]['wear']
              wearFour = jsonToPython['iteminfo']['stickers'][3]['wear']
            
            if len(jsonToPython['iteminfo']['stickers']) == 3: # If there are 3 stickers the following code is executed.
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']
              wearThree = jsonToPython['iteminfo']['stickers'][2]['wear']

            if len(jsonToPython['iteminfo']['stickers']) == 2: # If there are 2 stickers the following code is executed.
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']
              wearTwo = jsonToPython['iteminfo']['stickers'][1]['wear']

            if len(jsonToPython['iteminfo']['stickers']) == 1: # If there is 1 sticker the following code is executed.
              wearOne = jsonToPython['iteminfo']['stickers'][0]['wear']

              
              
            if len(jsonToPython['iteminfo']['stickers']) == 0: # If there are no stickers the following code is executed.
              stickerOutput =  ''
            #--- Sticker wear values. 
            else: # If there are stickers on the skin, the following code is executed.
              if len(jsonToPython['iteminfo']['stickers']) == 4: # If there are 4 stickers the following code is executed.
                
                if wearOne == None: # The code below is executed if the sticker wear is null.
                  wearOne = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearOne = wearOne*100 # Multiplies the wear of the sticker by 100 (to become a percent).

                if wearTwo == None: # The code below is executed if the sticker wear is null.
                  wearTwo = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearTwo = wearTwo*100 # Multiplies the wear of the sticker by 100 (to become a percent).

                if wearThree == None: # The code below is executed if the sticker wear is null.
                  wearThree = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearThree = wearThree*100# Multiplies the wear of the sticker by 100 (to become a percent).

                if wearFour == None: # The code below is executed if the sticker wear is null.
                  wearFour = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearFour = wearFour*100 # Multiplies the wear of the sticker by 100 (to become a percent).
              
              if len(jsonToPython['iteminfo']['stickers']) == 3: # If there are 3 stickers the following code is executed.
                
                if wearOne == None: # The code below is executed if the sticker wear is null.
                  wearOne = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearOne = wearOne*100 # Multiplies the wear of the sticker by 100 (to become a percent).

                if wearTwo == None: # The code below is executed if the sticker wear is null.
                  wearTwo = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearTwo = wearTwo*100 # Multiplies the wear of the sticker by 100 (to become a percent).

                if wearThree == None: # The code below is executed if the sticker wear is null.
                  wearThree = 0  # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearThree = wearThree*100 # Multiplies the wear of the sticker by 100 (to become a percent).

              if len(jsonToPython['iteminfo']['stickers']) == 2: # If there are 2 stickers the following code is executed.
                
                if wearOne == None: # The code below is executed if the sticker wear is null.
                  wearOne = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearOne = wearOne*100 # Multiplies the wear of the sticker by 100 (to become a percent).

                if wearTwo == None: # The code below is executed if the sticker wear is null.
                  wearTwo = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearTwo = wearTwo*100 # Multiplies the wear of the sticker by 100 (to become a percent).

              if len(jsonToPython['iteminfo']['stickers']) == 1: # If there is one sticker the following code is executed.
                
                if wearOne == None: # The code below is executed if the sticker wear is null.
                  wearOne = 0 # Assigns 0 as the wear value of the sticker.
                else: # If the sticker wear is not null the following code is executed.
                  wearOne = wearOne*100 # Multiplies the wear of the sticker by 100 (to become a percent).

              #--- Sticker output in embed.
              if len(jsonToPython['iteminfo']['stickers']) == 4: # If there are 4 stickers, the following code is executed.
                #- Stickers available with wear perecents as suffix. 
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerThree = '(' + str(wearThree)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][2]['name']
                stickerFour = '(' + str(wearFour)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][3]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo + '\n' + stickerThree + '\n' + stickerFour # Sticker output to be used in embed.

              if len(jsonToPython['iteminfo']['stickers']) == 3: # If there are 3 stickers, the following code is executed.
                #- Stickers available with wear perecents as suffix. 
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerThree = '(' + str(wearThree)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][2]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo + '\n' + stickerThree # Sticker output to be used in embed.

              if len(jsonToPython['iteminfo']['stickers']) == 2: # If there are 2 stickers, the following code is executed.
                #- Stickers available with wear perecents as suffix. 
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerTwo = '(' + str(wearTwo)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][1]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne + '\n' + stickerTwo # Sticker output to be used in embed.
              
              if len(jsonToPython['iteminfo']['stickers']) == 1: # If there is 1 sticker, the following code is executed.
                #- Stickers available with wear perecents as suffix. 
                stickerOne = '(' + str(wearOne)[0:2] +'%) ' + jsonToPython['iteminfo']['stickers'][0]['name']
                stickerOutput = '\n \n __**Stickers:**__ ' + '\n' +  stickerOne # Sticker output to be used in embed.
                
              
              


            if jsonToPython['iteminfo']['killeaterscoretype'] == None: # If the skin is not stat trak the following code is executed.
              rawMarketSkin = raw_skin + marketWear
            
            else: # If the skin is stat trak, the following code is executed. 
              rawMarketSkin = statSkin_raw + marketWear

            marketSkinOutput = rawMarketSkin.replace(' ', '+') # Replaces all spaces in the name of the skin with +'s, used for urls. 
            
            patternIndex = '**Index: **' + str(jsonToPython['iteminfo']['paintseed']) # Pattern index with suffix. # Pattern index with suffix, for use in embed. 
            
            

            for priceAPIData in urllib.request.urlopen('https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=' + marketSkinOutput): # Accesses steam API for skin prices. 
              jsonToPython = json.loads(priceAPIData.decode('utf-8')) # Loads steam api as json, decodes as utf-8. 

              if str('median_price') not in jsonToPython: # If the skin doesn't have an average price, the following code is executed. 
                marketMedianOutput = '**Avg. Price:** *Not available.*' # Suffix of not available added to avg price. 
              
              else: # If the skin does have an average price, the following code is executed. 
                marketMedian = jsonToPython['median_price'] # Assigns marketMedian the value of the skin's average price (str)
                marketMedianOutput = '**Avg. Price:** ' + marketMedian # marketMedian prefixed to avg price output, to be used in embed. 
            

            marketLink = 'https://steamcommunity.com/market/search?appid=730&q=' + marketSkinOutput # Link to market listings of the skin. 
            marketLinkOutput = '**Market: **[[Link]]' + '(' + marketLink + ')' # Market link as hyperklink, to be used in embed. 
            

            bitskinsLink = 'https://bitskins.com/?market_hash_name=' + marketSkinOutput + '&appid=730' # Link to bitskins listings of the skin. 
            bitskinsLinkOutput = '**Bitskins: **[[Link]]' + '(' + bitskinsLink + ')' # bitSKins link as hyperlink, to be used in embed.
            
            screenShotRedirOutput = '**Screenshot: ** [[Link]]' + '(' + screenShotRedir + ')'
            
            for apiData in urllib.request.urlopen('https://api.csgofloat.com/?url=' + inspectUrl): # Re-opens CSGOFloat api. 
              jsonToPython = json.loads(apiData.decode('utf-8')) # Loads data from API, decodes to utf-8. 

            if jsonToPython['iteminfo']['defindex'] in knifeID: # If the skin is a knife, the following code is executed. 
              #--- Adds knife star prefix. 
              msgOutput = '__**Information:**__ \n' + skin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput  

              msgOutputStat = '__**Information:**__ \n' + statSkin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n' + screenShotRedirOutput + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput 
            
            else: # If the skin is not a knife, the following code is executed. 
              msgOutput = '__**Information:**__ \n' + skin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) + '\n' + screenShotRedirOutput + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput + '\n' + stickerOutput 

              msgOutputStat = '__**Information:**__ \n' + statSkin + '\n' + suffixWear + '\n' + skin_floatValue + '\n' + str(patternIndex) +  '\n' + screenShotRedirOutput + '\n \n __**Listings:**__ \n' + marketLinkOutput + '\n' + bitskinsLinkOutput + '\n' + marketMedianOutput + stickerOutput
              

            if jsonToPython['iteminfo']['killeaterscoretype'] == None: # If the skin is not stat trak, the following code is executed. 
              #--- Final embed output, message printed to end user. 
              emb = discord.Embed(description= msgOutput, colour = 0x00b2ff) # Outputs data of the skin fetched from the inspect url. 
              emb.set_image(url=screenShotRedir) # Sets the embed as an image; screenShotRedir
              await client.send_message(message.channel, embed=emb) # Prints the embe
            
            else: # If the skin is stat trak, the following code is executed. 
              #--- Final embed output, message printed to end user. 
              emb = discord.Embed(description= msgOutputStat , colour = 0x00b2ff) # Outputs data of the skin fetched from the inspect url. 
              emb.set_image(url=screenShotRedir) # Sets the embed as an image; screenShotRedir
              await client.send_message(message.channel, embed=emb) # Prints the embed.
              
print(sys.argv[1])
client.run('NTI3MjU0OTY0MjU1MzI2MjI4.DwREYQ.Bo2ncCt3BYFA3e-GmNxtNLZaFMA') # Running bot with secret token.
#--- IMPORTANT: THIS TOKEN GIVES ACCESS TO BOT, DON'T LEAK. IF USED ON GITHUB MAKE SURE REPO IS PRIVATE 
