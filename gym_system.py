"""Fitness club class booking ledger."""
import glob
import json
import os

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class. Return True if booked."""
    if attendance_log is None:
        attendance_log = []
    member_id = str(member_id)
    if class_name not in class_capacity:
        print("Unknown class:", class_name)
        return False
    roster = rosters.setdefault(class_name, [])
    if member_id in roster:
        print("Already booked:", member_id)
        return False
    if len(roster) >= class_capacity[class_name]:
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Remove a member from a class roster."""
    try:
        rosters[class_name].remove(str(member_id))
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the capacity of a class (must be zero or more)."""
    if seats < 0:
        print("Invalid capacity:", seats)
        return
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Book walk-in guests into a class, stopping when it is full."""
    guest_number = 1
    booked = 0
    while booked < count:
        guest_id = f"GUEST-{guest_number}"
        guest_number += 1
        if guest_id in rosters.get(class_name, []):
            continue
        if not book_class(guest_id, class_name):
            break
        booked += 1


def export_roster(file="gym_schedule.json"):
    """Write all rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(rosters, handle)


def clear_old_exports(prefix="old_"):
    """Delete old exported JSON files."""
    for path in glob.glob(prefix + "*.json"):
        os.remove(path)


def show_rosters():
    """Print every class roster."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(members))


def main():
    """Run the demo."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    set_capacity("Spin", -2)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    raw = input("How many walk-in guests for HIIT? (Enter for 1): ") or "1"
    try:
        guests = int(raw)
    except ValueError:
        print("Please enter a whole number.")
        guests = 0
    add_members("HIIT", max(guests, 0))
    clear_old_exports()
    export_roster()
    show_rosters()


main()
