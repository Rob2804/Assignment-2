# =============================================================================
# Skill Swap Hub - Database Seeding Script
# COM4113 Tech Stack - Leeds Trinity University
# =============================================================================
# This script populates the MongoDB database with sample data so you can
# test the application without having to register users and post resources
# manually.
#
# Usage: python seed_data.py
#
# WARNING: This script will clear existing data in the users and resources
# collections before inserting sample data.
# =============================================================================

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# =============================================================================
# CONFIGURATION - Update with your own MongoDB Atlas connection string
# =============================================================================

MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"
DB_NAME = "skillswap_db"

# =============================================================================
# CONNECT TO DATABASE
# =============================================================================

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("Connected to MongoDB Atlas successfully.")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# =============================================================================
# CLEAR EXISTING DATA
# =============================================================================

confirm = input("This will DELETE all existing data. Type 'yes' to continue: ")
if confirm.lower() != "yes":
    print("Cancelled. No data was changed.")
    exit(0)

db["users"].delete_many({})
db["resources"].delete_many({})
print("Cleared existing collections.")

# =============================================================================
# SEED USERS
# =============================================================================

sample_users = [
    {
        "username": "alice_dev",
        "email": "alice@example.com",
        "password": generate_password_hash("password123"),
        "bio": "Computer science student who loves Python and web development.",
        "hobbies": "Programming, Reading, Gaming",
        "profile_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=14)
    },
    {
        "username": "bob_design",
        "email": "bob@example.com",
        "password": generate_password_hash("password123"),
        "bio": "Graphic design enthusiast learning to code.",
        "hobbies": "Design, Photography, Hiking",
        "profile_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=10)
    },
    {
        "username": "charlie_music",
        "email": "charlie@example.com",
        "password": generate_password_hash("password123"),
        "bio": "Music production student exploring AI tools.",
        "hobbies": "Music, AI Tools, Cooking",
        "profile_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=7)
    }
]

db["users"].insert_many(sample_users)
print(f"Inserted {len(sample_users)} sample users.")
print("  All sample users have the password: password123")

# =============================================================================
# SEED RESOURCES
# =============================================================================

sample_resources = [
    {
        "title": "Python for Beginners - Official Tutorial",
        "link": "https://docs.python.org/3/tutorial/",
        "description": "The official Python tutorial is brilliant for getting "
                       "started. It covers all the basics from variables to "
                       "classes in a clear, step-by-step format.",
        "category": "Programming",
        "author": "alice_dev",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=12)
    },
    {
        "title": "Figma Basics - Learn UI Design",
        "link": "https://www.figma.com/resources/learn-design/",
        "description": "Free resources from Figma to learn the fundamentals "
                       "of user interface design. Great for beginners who "
                       "want to build portfolio pieces.",
        "category": "Design",
        "author": "bob_design",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=9)
    },
    {
        "title": "Flask Mega-Tutorial by Miguel Grinberg",
        "link": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
        "description": "A comprehensive, free tutorial that walks you through "
                       "building a full web application with Flask. Covers "
                       "databases, forms, authentication and more.",
        "category": "Programming",
        "author": "alice_dev",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=8)
    },
    {
        "title": "Introduction to AI Music Production",
        "link": "https://www.soundonsound.com/",
        "description": "A collection of articles exploring how AI is changing "
                       "the music production landscape. Covers tools like "
                       "AIVA and Amper Music.",
        "category": "AI Tools",
        "author": "charlie_music",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=5)
    },
    {
        "title": "Basics of Food Photography",
        "link": "https://www.bbcgoodfood.com/howto/guide/how-photograph-food",
        "description": "Simple tips for taking better photos of your food. "
                       "Useful for anyone who wants to share recipes or "
                       "build an Instagram presence.",
        "category": "Photography",
        "author": "bob_design",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=3)
    },
    {
        "title": "Duolingo - Free Language Learning",
        "link": "https://www.duolingo.com/",
        "description": "The best free app for picking up a new language. "
                       "Gamified lessons keep you motivated and the daily "
                       "streaks help build a study habit.",
        "category": "Languages",
        "author": "charlie_music",
        "author_photo": "uploads/placeholder.png",
        "created_at": datetime.now() - timedelta(days=1)
    }
]

db["resources"].insert_many(sample_resources)
print(f"Inserted {len(sample_resources)} sample resources.")

# =============================================================================
# DONE
# =============================================================================
print("\nSeeding complete! You can now run the app with: python app.py")
print("Log in with any sample user (e.g. alice_dev / password123)")
