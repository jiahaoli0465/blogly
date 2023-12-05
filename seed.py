from models import db, User, Post, Tag, PostTag
from app import app  # Import the Flask app instance
import datetime

# Sample data
users = [
    {"first_name": "John", "last_name": "Doe"},
    {"first_name": "Jane", "last_name": "Doe"},
    {"first_name": "Alice", "last_name": "Smith"},
    {"first_name": "Bob", "last_name": "Brown"},
    {"first_name": "Charlie", "last_name": "Davis"},
    {"first_name": "Emily", "last_name": "Clark"},
    # Add more sample users here if needed
]

posts = [
    {"title": "My First Post", "content": "This is the content of my first post.", "user_index": 0},
    {"title": "A Day in the Life", "content": "Exploring a day in my life.", "user_index": 1},
    {"title": "The Joys of Cooking", "content": "Sharing my experiences and recipes in the kitchen.", "user_index": 2},
    {"title": "Tech Trends 2023", "content": "Discussing the latest in technology for this year.", "user_index": 3},
    {"title": "Travel Diaries: Paris", "content": "My unforgettable journey to Paris.", "user_index": 4},
    {"title": "Fitness Fundamentals", "content": "Tips and tricks for staying fit and healthy.", "user_index": 5},
    # Add more sample posts here if needed
]

tags = [
    {"name": "Life"},
    {"name": "Blog"},
    {"name": "Adventure"},
    {"name": "Travel"},
    {"name": "Food"},
    {"name": "Tech"},
    {"name": "Cooking"},
    {"name": "Recipes"},
    {"name": "Technology"},
    {"name": "Innovation"},
    {"name": "Fitness"},
    {"name": "Health"},
    # Add more sample tags here if needed
]

# Assign each post 4 tags
post_tags = []
for i in range(len(posts)):
    for j in range(4):  # Assign 4 tags to each post
        tag_index = (i * 4 + j) % len(tags)  # Cycle through tags
        post_tags.append({"post_index": i, "tag_index": tag_index})

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Add sample users
    user_objs = []
    for user_data in users:
        user = User(**user_data)
        db.session.add(user)
        user_objs.append(user)

    # Commit to get user IDs
    db.session.commit()

    # Add sample posts
    post_objs = []
    for post_data in posts:
        user = user_objs[post_data.pop("user_index")]
        post = Post(**post_data, user_id=user.id)
        db.session.add(post)
        post_objs.append(post)

    # Add sample tags
    tag_objs = []
    for tag_data in tags:
        tag = Tag(**tag_data)
        db.session.add(tag)
        tag_objs.append(tag)

    # Commit to get post and tag IDs
    db.session.commit()

    # Add post tags (associations)
    for pt in post_tags:
        post_tag = PostTag(post_id=post_objs[pt["post_index"]].id, tag_id=tag_objs[pt["tag_index"]].id)
        db.session.add(post_tag)

    # Final commit
    db.session.commit()
