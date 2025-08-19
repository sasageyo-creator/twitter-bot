# redeploy test

import tweepy
import os
import time

# Load keys from Render Environment
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

print("✅ Keys loaded successfully")

# Example stream listener
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Auto-like
            client.like(tweet.id)
            print(f"❤️ Liked tweet {tweet.id}")

            # Auto-retweet
            client.retweet(tweet.id)
            print(f"🔁 Retweeted {tweet.id}")

            # Auto-reply
            client.create_tweet(
                text="Thanks for tweeting! 🤖",
                in_reply_to_tweet_id=tweet.id
            )
            print(f"💬 Replied to {tweet.id}")

        except Exception as e:
            print(f"⚠️ Error handling tweet {tweet.id}: {e}")

def main():
    print("🚀 Bot is starting...")
    stream = MyStream(bearer_token=BEARER_TOKEN)

    # Add your filter rule (change keywords/hashtags)
    try:
        stream.add_rules(tweepy.StreamRule("python"))
    except Exception:
        pass  # Ignore if rule already exists

    print("🤖 Bot is now live and listening for tweets!")
    stream.filter(threaded=False)  # blocking, keeps running

if __name__ == "__main__":
    main()
