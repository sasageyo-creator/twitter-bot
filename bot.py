import tweepy
import requests
import os
import time
from datetime import datetime, timedelta

# --- Load environment variables ---
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
HF_TOKEN = os.getenv("HF_TOKEN")  # Hugging Face API token

# --- Authenticate with Twitter ---
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# --- Hugging Face Inference API ---
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_reply(text):
    """Generate AI-based reply using Hugging Face GPT-2"""
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            return data[0]["generated_text"][:200]  # Limit to 200 chars
        else:
            return "Thanks for mentioning me!"
    except Exception as e:
        print("⚠️ HuggingFace error:", e)
        return "Thanks for the mention!"

# --- Bot Setup ---
last_seen_id = None
start_time = datetime.now()
end_time = start_time + timedelta(hours=24)  # Stop after 24 hours

print("🤖 Bot started... Trial mode: 24h")

# --- Bot Loop ---
while True:
    try:
        # --- Stop after 24 hours ---
        if datetime.now() >= end_time:
            print("⏹️ Trial finished. Bot shutting down.")
            break

        # --- Check mentions ---
        mentions = api.mentions_timeline(since_id=last_seen_id, tweet_mode="extended")
        for mention in reversed(mentions):
            print(f"📌 New mention: {mention.user.screen_name} - {mention.full_text}")
            last_seen_id = mention.id

            # Auto like
            try:
                api.create_favorite(mention.id)
                print("❤️ Liked")
            except:
                print("❤️ Already liked")

            # Auto retweet
            try:
                api.retweet(mention.id)
                print("🔁 Retweeted")
            except:
                print("🔁 Already retweeted")

            # Auto reply with AI
            reply_text = generate_reply(mention.full_text)
            api.update_status(
                status=f"@{mention.user.screen_name} {reply_text}",
                in_reply_to_status_id=mention.id
            )
            print("💬 Replied")

        time.sleep(30)  # wait 30s before checking again

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(60)  # wait before retry