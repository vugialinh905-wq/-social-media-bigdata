# 📊 Social Media Big Data Storage & Analysis

> Hệ thống thu thập, lưu trữ và phân tích dữ liệu mạng xã hội sử dụng MongoDB

---

## 📋 Mô tả dự án

Dự án xây dựng pipeline lưu trữ và phân tích dữ liệu lớn từ các nền tảng mạng xã hội (Twitter, Reddit), phục vụ nghiên cứu hành vi người dùng và phân tích nội dung.

---

## 🗄️ Dataset

| Collection | Số lượng | Mô tả |
|---|---|---|
| `twitter_posts` | 162,969 | Bài đăng từ Twitter/X |
| `reddit_posts` | 37,149 | Bài đăng từ Reddit |
| `user_profiles` | 100 | Hồ sơ người dùng |
| `realtime_feeds` | 40 | Luồng dữ liệu thời gian thực |

**Tổng cộng: ~200,000+ documents**

---

## 🏗️ Cấu trúc dữ liệu

### Twitter Post
```json
{
  "_id": "ObjectId",
  "post_id": "tw_0",
  "text": "Nội dung bài đăng",
  "category": -1,
  "platform": "Twitter",
  "crawled_at": "ISODate"
}
```

### User Profile
```json
{
  "_id": "ObjectId",
  "user_id": "U0001",
  "username": "user_1",
  "platform": "Twitter",
  "followers": 4698,
  "total_posts": 62,
  "joined_date": "ISODate"
}
```

---

## 🛠️ Công nghệ sử dụng

- **Database:** MongoDB
- **Platform:** Linux (WSL2 / Ubuntu)
- **Tools:** MongoDB Shell (`mongosh`), MongoExport/Import
- **Language:** JavaScript (MongoDB queries)

---

## 🚀 Cài đặt & Chạy

### Yêu cầu
- MongoDB >= 5.0
- mongosh

### Cài đặt MongoDB
```bash
# Ubuntu/WSL
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### Clone & Import dữ liệu
```bash
git clone https://github.com/USERNAME/social-media-storage.git
cd social-media-storage

# Import dữ liệu mẫu
mongoimport --db social_media_db \
  --collection twitter_posts \
  --file sample_twitter.json

mongoimport --db social_media_db \
  --collection reddit_posts \
  --file sample_reddit.json
```

---

## 🔍 Truy vấn mẫu

```javascript
// Kết nối database
use social_media_db

// Xem 1 bài tweet
db.twitter_posts.findOne()

// Đếm tổng số bài theo platform
db.twitter_posts.countDocuments()

// Tìm user có nhiều followers nhất
db.user_profiles.find().sort({ followers: -1 }).limit(5)

// Thống kê bài đăng theo category
db.twitter_posts.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```





