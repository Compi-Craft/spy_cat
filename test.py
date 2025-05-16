import requests

BASE_URL = "http://localhost:8000"

def print_response(r):
    print(f"Status: {r.status_code}")
    print(r.json())
    print("-" * 40)

# 1. Створюємо кота
cat_data = {
    "name": "Whisker",
    "years_experience": 5,
    "breed": "Siberian",
    "salary": 3000.0
}
r = requests.post(f"{BASE_URL}/cats/", json=cat_data)
print("Created Spy Cat:")
print_response(r)
cat = r.json()
cat_id = cat["id"]

mission_data = {
    "targets": [
        {"name": "Target Alpha", "country": "Germany", "notes": ""},
        {"name": "Target Bravo", "country": "France", "notes": ""}
    ]
}
r = requests.post(f"{BASE_URL}/missions/", json=mission_data)
print("Created Mission:")
print_response(r)
mission = r.json()
mission_id = mission["id"]
target_ids = [t["id"] for t in mission["targets"]]

r = requests.put(f"{BASE_URL}/missions/{mission_id}/assign_cat", params={"cat_id": cat_id})
print("Assigned Cat to Mission:")
print_response(r)

for tid in target_ids:
    r = requests.put(f"{BASE_URL}/missions/targets/{tid}/notes", params={"notes": f"Initial notes for target {tid}"})
    print(f"Updated notes for target {tid}:")
    print_response(r)

for tid in target_ids:
    r = requests.put(f"{BASE_URL}/missions/targets/{tid}/complete")
    print(f"Completed target {tid}:")
    print_response(r)

r = requests.get(f"{BASE_URL}/missions/{mission_id}")
print("Final Mission State:")
print_response(r)

r = requests.put(f"{BASE_URL}/missions/targets/{target_ids[0]}/notes", params={"notes": "Too late!"})
print("Try updating completed target (should fail):")
print_response(r)
