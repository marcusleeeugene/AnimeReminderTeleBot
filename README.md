# Anime Reminder Telegram Bot <img src="/images/bot_dp.png" width="5%"/>
Telegram handle: @animereminder_bot 

## Introduction
Hello! This bot notifies you of new episode releases for Animes that you are watching.

It performs checks from 9Anime’s website. With this bot, you will never ever need to remember when a new episode will be released! :)

## How To:
To begin using the bot, add the telegram handle @animereminder_bot

<img src="/images/introduction.PNG" width="30%"> | <img src="/images/introduction.PNG" width="30%">


## Technical Stuff:
1) The bot is deployed onto Heroku Server.
2) Threading is used to support multiple users each time they start the bot.
3) It saves the Animes and the details that each user is tracking to Google's Firebase Real-time Database.
4) The bot scrapes data using BeautifulSoup4 and Selenium from 9Anime to check if there is a new episode release.
