import requests
import random
from datetime import datetime, timedelta

BASE_URL = "https://eventboard-backend.onrender.com"

forces = ["Army", "Navy", "Air Force", "BSF", "CRPF"]
ranks = ["Captain", "Lieutenant", "Major", "Commander", "Sergeant"]

# -------------------------------------------------------
# 1️⃣ Create Judges
# -------------------------------------------------------
print("🧑‍⚖️ Creating judges...")
judge_names = [
    "Col. Singh", "Cmdr. Sharma", "Lt. Mehta", "Maj. Nair", "Capt. Desai",
    "Lt. Col. Reddy", "Maj. Bhatia", "Col. Pillai", "Cmdr. Rao", "Capt. Gupta"
]

for i, name in enumerate(judge_names, start=1):
    payload = {
        "judge_id": i,  # ✅ include ID
        "name": name,
        "age": random.randint(35, 60),
        "force": random.choice(forces),
        "rank": random.choice(ranks),
    }
    r = requests.post(f"{BASE_URL}/judges", json=payload)
    if r.status_code not in [200, 201]:
        print(f"⚠️ Failed to add judge {name}: {r.text}")

print("✅ Judges created.\n")


# -------------------------------------------------------
# 2️⃣ Create Events
# -------------------------------------------------------
print("🏁 Creating events...")
event_names = [
    "Obstacle Course",
    "Rifle Marksmanship",
    "Grenade Throw Accuracy",
    "Endurance March",
    "Combat Fitness Test",
    "Tug of War (Unit Event)",
    "Battlefield Navigation",
    "Team Relay (Mixed Forces)"
]

start_date = datetime(2025, 2, 1)
for i, name in enumerate(event_names, start=1):
    payload = {
        "event_id": i,  # ✅ include ID
        "name": name,
        "round_name": f"Round {random.choice(['1', '2', '3', 'Final'])}",
        "event_date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    }
    r = requests.post(f"{BASE_URL}/events", json=payload)
    if r.status_code not in [200, 201]:
        print(f"⚠️ Failed to add event {name}: {r.text}")

print("✅ Events created.\n")


# -------------------------------------------------------
# 3️⃣ Create Players
# -------------------------------------------------------
print("🎖️ Creating players...")
first_names = [
    "Arjun", "Ravi", "Suresh", "Anita", "Priya", "Rahul", "Meena", "Vikas", "Sneha", "Ajay",
    "Sunita", "Vijay", "Amit", "Deepa", "Neha", "Kiran", "Rajesh", "Komal", "Manoj", "Rina",
    "Anil", "Seema", "Asha", "Rohit", "Nisha", "Gopal", "Ritu", "Varun", "Preeti", "Suman",
    "Harish", "Pooja", "Sanjay", "Geeta", "Akhil", "Rekha", "Mukesh", "Lata", "Santosh", "Tina"
]

for i, name in enumerate(first_names, start=1):
    payload = {
        "player_id": i,  # ✅ required by your API
        "name": name,
        "age": random.randint(20, 40),
        "force": random.choice(forces),
        "rank": random.choice(ranks),
    }
    r = requests.post(f"{BASE_URL}/players", json=payload)
    if r.status_code not in [200, 201]:
        print(f"⚠️ Failed to add player {name}: {r.text}")

print("✅ Players created.\n")


# -------------------------------------------------------
# 4️⃣ Create Scores
# -------------------------------------------------------
print("📊 Creating scores...")
players = requests.get(f"{BASE_URL}/players").json()
judges = requests.get(f"{BASE_URL}/judges").json()
events = requests.get(f"{BASE_URL}/events").json()

if not players or not judges or not events:
    print("❌ Missing base data. Ensure players, judges, and events exist first.")
else:
    score_start = datetime(2025, 11, 1)
    score_end = datetime(2025, 11, 8)

    for _ in range(500):
        player = random.choice(players)
        judge = random.choice(judges)
        event = random.choice(events)

        random_days = random.randint(0, (score_end - score_start).days)
        random_hours = random.randint(6, 22)
        random_minutes = random.randint(0, 59)
        score_date = score_start + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

        payload = {
            "event_id": event["event_id"],
            "player_id": player["player_id"],
            "judge_id": judge["judge_id"],
            "score": round(random.uniform(6.0, 10.0), 2),
            "score_date": score_date.isoformat()
        }

        r = requests.post(f"{BASE_URL}/scores/", json=payload)
        if r.status_code not in [200, 201]:
            print(f"⚠️ Failed to add score: {r.text}")

    print("✅ 500 random scores created successfully.\n")

print("🎉 Database seeding completed via API.")
