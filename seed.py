from app import app
from models import db, User, Post
import random
import lorem  # You might need to install this package using pip

# This assumes that your database configurations are already set in your app

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Creating a list of sample users
    users = [
        User(first_name='Alice', last_name='Johnson', image_url=None),
        User(first_name='Bob', last_name='Smith', image_url=None),
        User(first_name='Charlie', last_name='Brown', image_url=None),
        User(first_name='Diana', last_name='Prince', image_url=None),
        User(first_name='Edward', last_name='Norton', image_url=None)
    ]

    # Add sample users to the session
    for user in users:
        db.session.add(user)

    # Commit to save users to the database
    db.session.commit()

    # Create sample posts with lorem ipsum content
    for user in users:
        for _ in range(random.randint(2, 5)):  # Each user gets 2 to 5 posts
            title = lorem.sentence()
            content = lorem.paragraph()
            post = Post(title=title, content=content, user_id=user.id)
            db.session.add(post)

    # Commit to save posts to the database
    db.session.commit()

    print("Database seeded!")
