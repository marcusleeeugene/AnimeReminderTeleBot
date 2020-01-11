# Anime Reminder Telegram Bot <img src="/images/bot_dp.png" width="5%"/>
Telegram handle: @animereminder_bot 

## Introduction
Hello! This bot notifies you of new episode releases for Animes that you are watching.

It performs checks from 9Anime’s website. With this bot, you will never ever need to remember when a new episode will be released! :)

## How To Use:
To begin using the bot, add the telegram handle @animereminder_bot
<p align="center"> 
  <img src="/images/introduction.PNG" width="30%"/> 
  <img src="/images/add_command.PNG" width="30%"/>
  <img src="/images/9anime_search.PNG" width="30%"/>
</p>
<p>
  Begin by starting the bot with the "/start" command. Then do "/add" command. The bot will send you a link to 9Anime's
  website. Go ahead and search the Anime you would like to watch through the given link.
</p>
<p align="center"> 
  <img src="/images/anime_link.PNG" width="30%"/> 
  <img src="/images/added_anime.PNG" width="30%"/>
</p>
<p>
  After that, copy the link of the Anime and send it to the bot. It will notify you once the Anime has been added
  successfully.
</p>
<p align="center"> 
  <img src="/images/new_episode.PNG" width="30%"/> 
</p>
<p>
  Whenever there is a new episode release for the Anime you have added, it will send you a message that looks like this!
</p>

## Technical Stuff:
1) The bot is deployed onto Heroku Server.
2) Threading is used to support multiple users each time they start the bot.
3) It saves the Animes and the details that each user is tracking to Google's Firebase Real-time Database.
4) The bot scrapes data using Selenium from 9Anime to check if there is a new episode release.

(I have included the codes if you are interested. However do create your own API tokens to try it out.)
P.S. I did not include chromedriver and json key to firebase in this folder. Include your own! :)
