import os
import tweepy

# 🔑 Load Twitter API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Required for StreamingClient

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    raise ValueError("❌ Missing one or more Twitter API keys. Check your environment variables.")

# ✅ Authenticate with Twitter API v1.1 (needed for likes, retweets, replies)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# ✅ StreamingClient for real-time tweets
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"🐦 New Tweet: {tweet.text}")

        try:
            # ❤️ Like
            api.create_favorite(tweet.id)
            print("💙 Liked")

            # 🔁 Retweet
            api.retweet(tweet.id)
            print("🔁 Retweeted")

            # 💬 Reply
            reply_text = "This is an automated reply 👋"
            api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
            print("💬 Replied")

        except Exception as e:
            print(f"⚠️ Error handling tweet: {e}")

# ✅ Run bot
if __name__ == "__main__":
    print("🤖 Bot is running...")

    # Create stream
    stream = MyStream(bearer_token=BEARER_TOKEN)

    # Remove old rules (avoid duplicates)
    rules = stream.get_rules()
    if rules.data:
        rule_ids = [rule.id for rule in rules.data]
        stream.delete_rules(rule_ids)

    # Add tracking rule (edit this keyword)
    stream.add_rules(tweepy.StreamRule("python"))  # 🔑 Change "python" to what you want

    # Start stream
    stream.filter(tweet_fields=["referenced_tweets", "author_id"])
