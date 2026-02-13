"""
Lab 03: The Time Capsule - Demonstration Script
Saves and loads a character in all four formats, then compares results.
"""

import os
from character import Character


def main():
    # Create a test character
    hero = Character("Aragorn", 50)
    hero.gold = 10000
    hero.inventory = ["Sword", "Shield", "Potion"]
    hero.position = (42, 17)
    hero.experience = 99999

    print("=== Original Character ===")
    hero.display_stats()

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # --- Save in all formats ---
    # TODO: Uncomment each line as you implement the methods

    # hero.save_text("data/hero.txt")
    # hero.save_json("data/hero.json")
    # hero.save_binary("data/hero.bin")
    # hero.save_pickle("data/hero.pkl")

    # --- Compare file sizes ---
    # TODO: Uncomment after implementing all save methods
    #
    # formats = {
    #     'Custom Text': 'data/hero.txt',
    #     'JSON':        'data/hero.json',
    #     'Binary':      'data/hero.bin',
    #     'Pickle':      'data/hero.pkl'
    # }
    #
    # print("\n=== File Size Comparison ===")
    # for name, path in formats.items():
    #     size = os.path.getsize(path)
    #     print(f"{name:15s}: {size:5d} bytes")

    # --- Verify round-trips ---
    # TODO: Uncomment after implementing all load methods
    #
    # print("\n=== Round-Trip Verification ===")
    # loaded_text = Character.load_text("data/hero.txt")
    # loaded_json = Character.load_json("data/hero.json")
    # loaded_bin  = Character.load_binary("data/hero.bin")
    # loaded_pkl  = Character.load_pickle("data/hero.pkl")
    #
    # for label, loaded in [("Text", loaded_text), ("JSON", loaded_json),
    #                        ("Binary", loaded_bin), ("Pickle", loaded_pkl)]:
    #     match = (loaded.name == hero.name and loaded.level == hero.level
    #              and loaded.gold == hero.gold)
    #     print(f"{label:8s} round-trip: {'PASS' if match else 'FAIL'}")

    # --- Checksum demo ---
    # TODO: Uncomment after implementing checksum methods
    #
    # print("\n=== Checksum Validation ===")
    # hero.save_json_with_checksum("data/hero_checked.json")
    # loaded = Character.load_json_with_checksum("data/hero_checked.json")
    # print(f"Checksum verified: {loaded.name}")


if __name__ == "__main__":
    main()
