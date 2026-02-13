"""
Lab 03: The Time Capsule - Character Save System
Character class with multiple serialization formats.
"""

import json
import struct
import pickle
import hashlib


class Character:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.health = 100 * level
        self.max_health = 100 * level
        self.mana = 50 * level
        self.max_mana = 50 * level
        self.position = (0, 0)
        self.inventory = []
        self.gold = 100
        self.experience = 0

    def __repr__(self):
        return f"Character(name='{self.name}', level={self.level})"

    def display_stats(self):
        print(f"--- {self.name} (LVL {self.level}) ---")
        print(f"HP: {self.health}/{self.max_health} | MP: {self.mana}/{self.max_mana}")
        print(f"Pos: {self.position} | Gold: {self.gold}")
        print(f"Items: {', '.join(self.inventory) if self.inventory else 'None'}")

    def to_dict(self):
        """Convert character state to a plain dictionary."""
        return {
            'name': self.name,
            'level': self.level,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'position': list(self.position),
            'inventory': self.inventory.copy(),
            'gold': self.gold,
            'experience': self.experience
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Character from a dictionary."""
        character = cls(data['name'], data['level'])
        character.health = data['health']
        character.max_health = data['max_health']
        character.mana = data['mana']
        character.max_mana = data['max_mana']
        character.position = tuple(data['position'])
        character.inventory = data['inventory'].copy()
        character.gold = data['gold']
        character.experience = data['experience']
        return character

    # -------------------------------------------------------------------------
    # Method 1: Custom Text Format
    # -------------------------------------------------------------------------

    def save_text(self, filepath):
        """Save character to custom text format."""
        with open(filepath, 'w') as f:
            f.write("[CHARACTER]\n")
            f.write(f"name={self.name}\n")
            f.write(f"level={self.level}\n")
            f.write(f"health={self.health}\n")
            f.write(f"max_health={self.max_health}\n")
            f.write(f"mana={self.mana}\n")
            f.write(f"max_mana={self.max_mana}\n")
            f.write(f"position={self.position[0]},{self.position[1]}\n")
            f.write(f"gold={self.gold}\n")
            f.write(f"experience={self.experience}\n")
            f.write("[INVENTORY]\n")
            for item in self.inventory:
                f.write(f"{item}\n")

    @classmethod
    def load_text(cls, filepath):
        """Load character from custom text format."""
        # TODO: Implement - see lab03.md Part B for hints
        pass

    # -------------------------------------------------------------------------
    # Method 2: JSON Format
    # -------------------------------------------------------------------------

    def save_json(self, filepath):
        """Save character to JSON format."""
        # TODO: Implement - wrap self.to_dict() in {"character": ...}
        pass

    @classmethod
    def load_json(cls, filepath):
        """Load character from JSON format."""
        # TODO: Implement - extract data['character'], use cls.from_dict()
        pass

    # -------------------------------------------------------------------------
    # Method 3: Binary Format (struct)
    # -------------------------------------------------------------------------

    HEADER_FORMAT = '32s10i'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 72 bytes

    def save_binary(self, filepath):
        """Save character to binary format using struct."""
        # TODO: Implement - see lab03.md Part D for layout details
        pass

    @classmethod
    def load_binary(cls, filepath):
        """Load character from binary format."""
        # TODO: Implement - unpack header, read inventory
        pass

    # -------------------------------------------------------------------------
    # Method 4: Pickle Format
    # -------------------------------------------------------------------------

    def save_pickle(self, filepath):
        """Save character using pickle."""
        # TODO: Implement
        pass

    @classmethod
    def load_pickle(cls, filepath):
        """Load character from pickle file."""
        # TODO: Implement
        pass

    # -------------------------------------------------------------------------
    # Data Integrity: Checksum
    # -------------------------------------------------------------------------

    def save_json_with_checksum(self, filepath):
        """Save character to JSON with MD5 integrity checksum."""
        # TODO: Implement - see lab03.md Phase 3 for the wrapper pattern
        pass

    @classmethod
    def load_json_with_checksum(cls, filepath):
        """Load character from JSON and verify checksum integrity."""
        # TODO: Implement - recompute checksum and compare
        pass
