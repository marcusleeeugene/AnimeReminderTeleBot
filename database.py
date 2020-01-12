import pyrebase, os

#https://github.com/thisbejim/Pyrebase#database
#https://firebase.google.com/docs/database/admin/save-data
config = {
  "apiKey": "<API KEY>",
  "authDomain": "<AUTH DOMAIN>",
  "databaseURL": "<DATABASE URL>",
  "storageBucket": "<STORAGE BUCKET>",
  "serviceAccount": os.getcwd() + "<JSON SERVICE KEY>"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

def server_restart_prev_subscribed_users(): #returns all users who were previously subscribed before the server went down
    all_users_prev_subscribed = []
    all_users = list(dict(db.child("users").get().val()))
    all_users.remove("Admin_Bot")
    for user in all_users:
        if dict(db.child("users").child(user).get().val())["Subscription"] == "true":
            all_users_prev_subscribed.append([user, dict(db.child("users").child(user).get().val())["Chat_id"]])
    return all_users_prev_subscribed #Index 0 for username, Index 1 for chat_id

def create_user_db(user_id, chat_id):
    all_users = db.child("users").get().val()
    #Check if user exists
    if user_id not in all_users: #If user do not exist, create user
        data = {"Subscription": "false", "Chat_id": chat_id}
        db.child("users").child(user_id).set(data)
    else:
        data = {"Subscription": "false", "Chat_id": chat_id}
        db.child("users").child(user_id).update(data)

def subscribe_to_reminder(user_id):
    data = {"Subscription": "true"}
    db.child("users").child(user_id).update(data)

def unsubscribe_from_reminder(user_id):
    data = {"Subscription": "false"}
    db.child("users").child(user_id).update(data)

def check_subscription(user_id): #Returns true if user is subscribed to reminder
    subscription_status = dict(db.child("users").child(user_id).get().val())["Subscription"]
    if subscription_status == "false":
        return False
    else:
        return True

def add_anime_db(user_id, anime_details):
    data = {anime_details[0]: "true"}
    db.child("users").child(user_id).update(data) #add in Anime into user_id
    data = {"Status": anime_details[1], "Episode": anime_details[2]} #add in Anime details under Anime name
    db.child("users").child(user_id).child(anime_details[0]).update(data)

def get_anime_list_db(user_id): #list of anime user is keeping track of
    list_of_animes = list(dict(db.child("users").child(user_id).get().val()).keys())
    list_of_animes.remove("Subscription")
    list_of_animes.remove("Chat_id")
    return list_of_animes

def get_anime_details_db(user_id, anime_name):
    latest_episode_in_db = dict(db.child("users").child(user_id).child(anime_name).get().val())["Episode"]
    status_in_db = dict(db.child("users").child(user_id).child(anime_name).get().val())["Status"]
    anime_details = [status_in_db, latest_episode_in_db] #index 0 for status of anime, index 1 for latest ep
    return anime_details

def update_anime_details_db(user_id, anime_details):
    data = {"Status": anime_details[1], "Episode": anime_details[2]} #add in Anime details under Anime name
    db.child("users").child(user_id).child(anime_details[0]).update(data)

def remove_anime_db(user_id, anime_name):
    db.child("users").child(user_id).child(anime_name).remove()
