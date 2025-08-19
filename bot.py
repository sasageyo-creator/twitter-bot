import tweepy
import os
import time
import random

# Load credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Debugging: check if keys are loaded
print("API_KEY loaded:", API_KEY is not None)
print("API_SECRET loaded:", API_SECRET is not None)
print("ACCESS_TOKEN loaded:", ACCESS_TOKEN is not None)
print("ACCESS_SECRET loaded:", ACCESS_SECRET is not None)

# Exit early if any key is missing
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    raise ValueError("❌ One or more Twitter API keys are missing. Please check your environment variables.")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

print("✅ Bot is running...")

# Function to generate a simple AI-like reply
def generate_reply(tweet_text):
    replies = [
        "Thanks for sharing your thoughts!",
        "Interesting perspective! 🤔",
        "Totally agree with this 👍",
        "I hadn’t thought of it that way before.",
        "Great point!"
    ]
    return random.choice(replies)

# Stream Listener
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print(f"👀 New tweet from @{status.user.screen_name}: {status.text}")
            
            # Like
            api.create_favorite(status.id)
            print("❤️ Liked the tweet")

            # Retweet
            api.retweet(status.id)
            print("🔁 Retweeted the tweet")

            # Reply
            reply_text = f"@{status.user.screen_name} {generate_reply(status.text)}"
            api.update_status(status=reply_text, in_reply_to_status_id=status.id)
            print("💬 Replied to the tweet")

        except Exception as e:
            print("Error:", e)

# Run the stream (listening for mentions)
while True:
    try:
        print("🚀 Starting stream...")
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=["@YourTwitterHandle"], is_async=False)
    except Exception as e:
        print("Stream crashed, restarting in 15s. Error:", e)
        time.sleep(15)
