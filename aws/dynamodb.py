import os
import requests
import json



link = "https://phoneleaderboard.andrewslayton.dev/api"

def create_user(username):
    try:
       requests.post(link + "/user" , json={"username": username})
    except Exception as e:
        print("Error creating user:", e)

def increment_phone_usage(username):
    """Increment the phone usage counter for a user."""
    try:
        requests.post(link + "/data" , json={"username": username})
    except Exception as e:
        print("Error incrementing phone usage:", e)
        
def user_exists(username):
    try:
        response = requests.post(link + "/login" , json={"username": username})
    except Exception as e:
        print("Error checking if user exists:", e)
    if response.status_code == 200:
        return True 
    else :
        return False
