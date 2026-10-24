import feedparser
import requests
import json
import os

# 1. Telegram Bilgilerin
BOT_TOKEN = "8836706341:AAGMVs0mcDqyBw33RbaNxkGhRCUhp8Dds6M"
CHAT_ID = "-1004358035234"  # Örn: "-1001234567890"

# 2. Takip Edilecek Araştırmacıların RSS / Blog Kaynakları
FEEDS = {
    "Simon Willison (LLM Security)": "https://simonwillison.net/atom/entries/",
    "Johann Rehberger (Embrace The Red)": "https://embracethered.com/blog/index.xml",
    "Troy Hunt (Web Security)": "https://www.troyhunt.com/rss/",
    "Gergely Orosz (Pragmatic Engineer)": "https://newsletter.pragmaticengineer.com/feed",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
}

HISTORY_FILE = "sent_posts.json"

def load_sent_posts():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_sent_posts(posts):
    with open(HISTORY_FILE, "w") as f:
        json.dump(posts, f)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def check_feeds():
    sent_posts = load_sent_posts()
    new_sent = list(sent_posts)

    for author, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: # Son 3 yazıya bak
                post_id = entry.link
                if post_id not in sent_posts:
                    title = entry.title
                    link = entry.link
                    
                    message = f"🚨 <b>{author}</b> Yeni Paylaşım!\n\n" \
                              f"📌 <b>{title}</b>\n\n" \
                              f"🔗 <a href='{link}'>Makaleyi Oku</a>"
                    
                    send_telegram_message(message)
                    new_sent.append(post_id)
        except Exception as e:
            print(f"Hata ({author}): {e}")

    # Çok büyümesin diye son 200 gönderiyi sakla
    save_sent_posts(new_sent[-200:])

if __name__ == "__main__":
    check_feeds()
