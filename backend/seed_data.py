# backend/seed_data.py
from backend.database import SessionLocal
from backend.models import Player, Judge, Event
from datetime import datetime, timedelta
import random

# -------------------------------------------------------
# Connect to DB session
# -------------------------------------------------------
db = SessionLocal()

# -------------------------------------------------------
# 1️⃣ Players (100 total)
# -------------------------------------------------------
first_names = [
    "Arjun", "Ravi", "Suresh", "Anita", "Priya", "Rahul", "Meena", "Vikas", "Sneha", "Ajay",
    "Sunita", "Vijay", "Amit", "Deepa", "Neha", "Kiran", "Rajesh", "Komal", "Manoj", "Rina",
    "Anil", "Seema", "Asha", "Rohit", "Nisha", "Gopal", "Ritu", "Varun", "Preeti", "Suman",
    "Harish", "Pooja", "Sanjay", "Geeta", "Akhil", "Rekha", "Mukesh", "Lata", "Santosh", "Tina",
    "Hemant", "Divya", "Yogesh", "Pinky", "Rakesh", "Shalini", "Kavita", "Vivek", "Naveen", "Manish",
    "Chirag", "Simran", "Nitin", "Sakshi", "Abhishek", "Tanvi", "Lokesh", "Bhavna", "Mohit", "Neelam",
    "Parveen", "Rupesh", "Dipika", "Himanshu", "Namita", "Tejas", "Isha", "Roshan", "Kirti", "Jayant",
    "Rachit", "Shruti", "Mayank", "Radhika", "Suraj", "Amrita", "Tarun", "Aarti", "Akhila", "Deepak",
    "Rajiv", "Mitali", "Gautam", "Anju", "Rehan", "Irfan", "Nivedita", "Umesh", "Kartik", "Lavanya",
    "Ramesh", "Aditi", "Ananya", "Sahil", "Bharat", "Ragini", "Vinay", "Payal", "Aniket", "Farhan"
]

forces = ["Army", "Navy", "Air Force", "BSF", "CRPF"]
ranks = ["Captain", "Lieutenant", "Major", "Commander", "Sergeant"]

players = []
for i, name in enumerate(first_names[:100], start=1):
    player = Player(
        player_id=i,
        name=name,
        age=random.randint(20, 40),
        force=random.choice(forces),
        rank=random.choice(ranks)
    )
    players.append(player)

# -------------------------------------------------------
# 2️⃣ Judges (12 total)
# -------------------------------------------------------
judge_names = [
    "Col. Singh", "Cmdr. Sharma", "Lt. Mehta", "Maj. Nair", "Capt. Desai", "Lt. Col. Reddy",
    "Maj. Bhatia", "Col. Pillai", "Cmdr. Rao", "Capt. Gupta", "Lt. Patel", "Maj. Khanna"
]

judges = []
for name in judge_names:
    judge = Judge(
        name=name,
        age=random.randint(35, 60),
        force=random.choice(forces),
        rank=random.choice(ranks)
    )
    judges.append(judge)

# -------------------------------------------------------
# 3️⃣ Events (8 total)
# -------------------------------------------------------
event_names = [
    "100m Sprint",
    "Long Jump",
    "High Jump",
    "Shooting (Rifle)",
    "Swimming Freestyle",
    "Weightlifting",
    "Marathon",
    "Boxing Finals"
]

events = []
start_date = datetime(2025, 2, 1)
for i, name in enumerate(event_names, start=1):
    event = Event(
        name=name,
        round_name=f"Round {random.choice(['1', '2', '3', 'Final'])}",
        event_date=start_date + timedelta(days=i)
    )
    events.append(event)

# -------------------------------------------------------
# Commit everything
# -------------------------------------------------------
try:
    db.add_all(players)
    db.add_all(judges)
    db.add_all(events)
    db.commit()
    print("✅ Database seeded successfully with 100 Players, 12 Judges, and 8 Events!")
except Exception as e:
    db.rollback()
    print(f"❌ Error seeding database: {e}")
finally:
    db.close()
