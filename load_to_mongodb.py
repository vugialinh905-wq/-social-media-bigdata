import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import random

# ── Kết nối MongoDB ──────────────────────────────────
client = MongoClient("mongodb://localhost:27017/")
db = client["social_media_db"]

print("=" * 60)
print("   LOADING SOCIAL MEDIA DATA INTO MONGODB")
print("=" * 60)

# ==============================================================
# [1] LOAD TWITTER POSTS
# ==============================================================
print("\n[1] LOADING TWITTER DATA...")

twitter_df = pd.read_csv("data/Twitter_Data.csv")
twitter_df = twitter_df.dropna()

twitter_collection = db["twitter_posts"]
twitter_collection.delete_many({})  # clear cũ nếu có

twitter_records = []
for idx, row in twitter_df.iterrows():
    doc = {
        "post_id": f"tw_{idx}",
        "text": row["clean_text"],
        "category": int(row["category"]),
        "platform": "Twitter",
        "crawled_at": datetime.now()
    }
    twitter_records.append(doc)

twitter_collection.insert_many(twitter_records)
print(f"    ✓ Inserted {len(twitter_records):,} Twitter posts")

# ==============================================================
# [2] LOAD REDDIT POSTS
# ==============================================================
print("\n[2] LOADING REDDIT DATA...")

reddit_df = pd.read_csv("data/Reddit_Data.csv")
reddit_df = reddit_df.dropna()

reddit_collection = db["reddit_posts"]
reddit_collection.delete_many({})

reddit_records = []
for idx, row in reddit_df.iterrows():
    doc = {
        "post_id": f"rd_{idx}",
        "text": row["clean_comment"],
        "category": int(row["category"]),
        "platform": "Reddit",
        "crawled_at": datetime.now()
    }
    reddit_records.append(doc)

reddit_collection.insert_many(reddit_records)
print(f"    ✓ Inserted {len(reddit_records):,} Reddit posts")

# ==============================================================
# [3] TẠO USER PROFILES (mô phỏng từ dữ liệu)
# ==============================================================
print("\n[3] GENERATING USER PROFILES...")

user_collection = db["user_profiles"]
user_collection.delete_many({})

usernames = [f"user_{i}" for i in range(1, 101)]
user_records = []

for i, username in enumerate(usernames):
    doc = {
        "user_id": f"U{i+1:04d}",
        "username": username,
        "platform": random.choice(["Twitter", "Reddit"]),
        "followers": random.randint(10, 5000),
        "total_posts": random.randint(1, 200),
        "joined_date": datetime(2020, random.randint(1,12), random.randint(1,28))
    }
    user_records.append(doc)

user_collection.insert_many(user_records)
print(f"    ✓ Inserted {len(user_records):,} user profiles")

# ==============================================================
# [4] TẠO REALTIME FEEDS COLLECTION (mô phỏng)
# ==============================================================
print("\n[4] CREATING REALTIME FEEDS COLLECTION...")

feeds_collection = db["realtime_feeds"]
feeds_collection.delete_many({})

sample_posts = twitter_records[:20] + reddit_records[:20]
feed_records = []

for post in sample_posts:
    doc = {
        "feed_id": f"feed_{post['post_id']}",
        "post_id": post["post_id"],
        "platform": post["platform"],
        "text_preview": post["text"][:100],
        "timestamp": datetime.now(),
        "is_trending": random.choice([True, False])
    }
    feed_records.append(doc)

feeds_collection.insert_many(feed_records)
print(f"    ✓ Inserted {len(feed_records):,} realtime feed entries")

# ==============================================================
# [5] SUMMARY
# ==============================================================
print("\n" + "=" * 60)
print("   DATABASE SUMMARY")
print("=" * 60)
print(f"   twitter_posts     : {twitter_collection.count_documents({}):,}")
print(f"   reddit_posts      : {reddit_collection.count_documents({}):,}")
print(f"   user_profiles     : {user_collection.count_documents({}):,}")
print(f"   realtime_feeds    : {feeds_collection.count_documents({}):,}")
print("=" * 60)
print("   ALL DATA LOADED SUCCESSFULLY!")
print("=" * 60)

client.close()
