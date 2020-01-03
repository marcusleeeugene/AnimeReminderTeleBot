#https://github.com/eternnoir/pyTelegramBotAPI#getting-started
import telebot, webcrawler, database, time as _time, schedule, threading, datetime
import logging
from telebot import types
from webcrawler import *
from database import *
from datetime import *

TOKEN = "<TELEGRAM TOKEN>"
HEROKU_WEB_URL = "<HEROKU URL>"
bot = telebot.TeleBot(TOKEN, threaded=False)

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

listofcommands = ("Here are the commands available:\n"
"/add - Adds a new anime to keep track of.\n"
"/remove - Removes an anime that you no longer want to keep track of.\n"
"/tracklist - Shows the current list of animes you are keeping track of.\n"
"/help - Shows the list of commands available for this bot.\n"
"/stop - Stops the bot.")

total_started_threads = [] #Used to keep track of users who already started threads. Resets when program crashes.

# =========================================================================================
# List of commands for bot
# =========================================================================================

#/start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    introduction = "Hello! This bot will help you keep track of the Animes you are watching! It will notify you each time the anime you are keeping track of releases a new episode.\n\n"
    bot.reply_to(message, introduction + listofcommands)
    create_user_db(message.from_user.username) #set user subscription to false and create user if they don't exist
    #The following is to prevent unecessary threads to be created
    if message.from_user.username in total_started_threads:
        subscribe_to_reminder(message.from_user.username)
    else:
        subscribe_to_reminder(message.from_user.username)
        init_episode_reminder = threading.Thread(target=new_episode_reminder_timer, kwargs={'user_id': message.from_user.username, 'chat_id': message.chat.id})
        init_episode_reminder.daemon = True
        init_episode_reminder.start()
        total_started_threads.append(message.from_user.username)
    print(total_started_threads)

#/add command
@bot.message_handler(commands=['add'])
def send_add(message):
    prompt = ("What Anime would you like to add?\n\nSearch from this link and copy paste the Anime's link into the reply box.\nhttps://9anime.xyz/")
    sentmsg = bot.send_message(message.chat.id, prompt, reply_markup=types.ForceReply(selective=True)) #Forces user to reply to msg
    bot.register_for_reply(sentmsg, add_anime_to_list)

#/remove command
@bot.message_handler(commands=['remove'])
def send_remove(message):
    prompt = ("What Anime would you like to remove? (Input the number)\n")
    index = 1
    for each in get_anime_list_db(message.from_user.username):
        prompt += "{}{}{}".format(index,") ", each) + "\n"
        index +=1
    sentmsg = bot.send_message(message.chat.id, prompt, reply_markup=types.ForceReply(selective=True)) #Forces user to reply to msg
    bot.register_for_reply(sentmsg, remove_anime_from_list)

#/tracklist command
@bot.message_handler(commands=['tracklist'])
def send_tracklist(message):
    prompt = ("Here's the list of Animes you are keeping track of:\n\n")
    index = 1
    for each in get_anime_list_db(message.from_user.username):
        prompt += "{}{}{}".format(index,") ", each) + "\n"
        index +=1
    bot.reply_to(message, prompt)
    #bot.send_message(message.chat.id, listofcommands)

#/help command
@bot.message_handler(commands=['help'])
def send_commands(message):
    instructions = ("Here are some commands to get you started!\n"
    "/add - Adds a new anime to keep track of.\n"
    "/remove - Removes an anime that you no longer want to keep track of.\n"
    "/tracklist - Shows the current list of animes you are keeping track of.\n"
    "/help - Shows the list of commands available for this bot.\n"
    "/stop - Stops the bot.")
    bot.reply_to(message, instructions)

#/stop command
@bot.message_handler(commands=['stop'])
def send_commands(message):
    unsubscribe_from_reminder(message.from_user.username)
    bot.reply_to(message, "Thank you for using the bot!\nFeel free to start the bot again with:\n/start")

# =========================================================================================
# Functional logic of bot
# =========================================================================================
def add_anime_to_list(message): #message will be in the form of url
    add_anime_db(message.from_user.username, set_anime_details(message.text))
    bot.send_message(message.chat.id, message.text + " has been added!\n\n")
    #bot.send_message(message.chat.id, listofcommands)

def remove_anime_from_list(message):
    if(message.text.isnumeric() and int(message.text) > 0):
        anime_to_remove = get_anime_list_db(message.from_user.username)[int(message.text) - 1]
        remove_anime_db(message.from_user.username, anime_to_remove)
        bot.send_message(message.chat.id, "The anime has been removed!")
    else:
        bot.send_message(message.chat.id, "Failed to remove. Please check if you input the number correctly!")
    #bot.send_message(message.chat.id, listofcommands)

def new_episode_reminder(user_id, chat_id):
    for anime in get_anime_list_db(user_id):
        if get_anime_details_db(user_id, anime)[0] == "Ongoing" and get_anime_details_db(user_id, anime)[1] != check_num_episodes(anime):
            update_anime_details_db(user_id, get_anime_details_by_name(anime))
            watch_url = "https://9anime.xyz/watch/" + format_anime_name(anime) + "/ep-" + check_num_episodes(anime)
            bot.send_message(chat_id, "New episode release:\n" + anime + " [EP:"+ check_num_episodes(anime) + " ]\n" + watch_url)

def new_episode_reminder_timer(user_id, chat_id):
    while True:
        if datetime.now().minute == 0 and check_subscription(user_id) == True:
            new_episode_reminder(user_id, chat_id)
            #bot.send_message(chat_id, "Hourly check complete.") #Use this to ensure bot is running this every hour for testing purpose
        _time.sleep(60) #Re-runs function every 60seconds


#Start Bot
bot.polling(none_stop=True)
