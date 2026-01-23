#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 01: The Rosetta Frequency - Reference Implementation
COMP3084 - Data Structures for Data Science

This module contains the TextAnalyzer and CodeAnalyzer classes
for linguistic forensics analysis through letter frequency analysis.
"""

import re


class TextAnalyzer:
    """
    A forensic tool for analyzing text files and extracting
    linguistic fingerprints through letter frequency analysis.

    Attributes:
        filepath (str): Path to the text file to analyze
        content (str): The raw text content
        frequency_map (dict): Dictionary storing character frequencies
    """

    def __init__(self, filepath):
        """
        Initialize the analyzer with a file path.

        Args:
            filepath (str): Path to the text file to analyze
        """
        self.filepath = filepath
        self.content = ""
        self.frequency_map = {}

    def load_file(self):
        """
        Load the file content with encoding detection.
        Tries UTF-8 first, falls back to Latin-1 if needed.

        Handles FileNotFoundError and UnicodeDecodeError gracefully.
        """
        try:
            # Attempt to read with UTF-8 encoding (most common)
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()

        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
            self.content = ""

        except UnicodeDecodeError:
            # Fallback to Latin-1 encoding for Western European text
            try:
                with open(self.filepath, 'r', encoding='latin-1') as f:
                    self.content = f.read()
                print(f"Warning: '{self.filepath}' read with Latin-1 encoding (not UTF-8)")
            except Exception as e:
                print(f"Error reading file '{self.filepath}': {e}")
                self.content = ""

    def clean_content(self):
        """
        Clean the content by:
        - Converting to lowercase
        - Removing all non-alphabetic characters (keep only a-z)

        This standardizes the text for frequency analysis.
        """
        # Convert to lowercase
        self.content = self.content.lower()

        # Keep only alphabetic characters (a-z)
        self.content = ''.join(char for char in self.content if char.isalpha())

    def calculate_frequency(self):
        """
        Count the frequency of each letter in the cleaned content.
        Populates self.frequency_map with letter counts.
        """
        # Reset frequency map
        self.frequency_map = {}

        # Count each character
        for char in self.content:
            self.frequency_map[char] = self.frequency_map.get(char, 0) + 1

    def report(self):
        """
        Print a formatted report of the analysis results.
        Shows:
        - Filename
        - Total character count
        - Top 5 most frequent letters with counts and percentages
        """
        # Calculate total characters
        total_chars = sum(self.frequency_map.values())

        # Sort by frequency (descending)
        sorted_items = sorted(
            self.frequency_map.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Get top 5
        top_5 = sorted_items[:5]

        # Print report
        print("=" * 50)
        print(f"Analysis Report: {self.filepath}")
        print("=" * 50)
        print(f"Total characters analyzed: {total_chars}")
        print(f"\nTop 5 most frequent letters:")

        for i, (letter, count) in enumerate(top_5, 1):
            percentage = (count / total_chars) * 100 if total_chars > 0 else 0
            print(f"  {i}. '{letter}': {count:5d} ({percentage:5.2f}%)")

        print("=" * 50)


class CodeAnalyzer(TextAnalyzer):
    """
    Specialized analyzer for source code files.
    Inherits from TextAnalyzer but overrides cleaning logic
    to remove programming-specific noise.

    This allows for linguistic analysis of variable names and
    comments without interference from programming keywords and syntax.
    """

    def clean_content(self):
        """
        Clean source code by removing:
        - Comments (# to end of line in Python)
        - Common Python keywords
        - Syntax characters (_ : ( ) " ' { } [ ])
        Then apply standard text cleaning (lowercase, alpha only).

        This reveals the underlying language used in comments
        and variable naming.
        """
        # Remove single-line comments (# to end of line)
        self.content = re.sub(r'#.*', '', self.content)

        # Remove common Python keywords that skew frequency
        keywords = (
            r'\b(def|class|return|import|if|else|elif|for|while|'
            r'self|try|except|finally|with|as|in|from|and|or|not|'
            r'is|True|False|None|break|continue|pass|raise|assert|'
            r'lambda|yield|global|nonlocal|del|print|input)\b'
        )
        self.content = re.sub(keywords, '', self.content)

        # Remove common syntax characters
        syntax_chars = ['_', '(', ')', ':', '"', "'", '{', '}', '[', ']',
                        ',', '.', ';', '=', '+', '-', '*', '/', '\\',
                        '<', '>', '!', '?', '@', '%', '&', '|', '^', '~']

        for char in syntax_chars:
            self.content = self.content.replace(char, ' ')

        # Apply standard cleaning (lowercase, alphabetic only)
        self.content = self.content.lower()
        self.content = ''.join(char for char in self.content if char.isalpha())


# Demonstration and testing
if __name__ == "__main__":
    print("=" * 70)
    print(" Lab 01: The Rosetta Frequency - Analyzer Module Test")
    print("=" * 70)
    print()

    # Test TextAnalyzer on English control
    print("Testing TextAnalyzer on English control sample...")
    eng = TextAnalyzer('../data/english.txt')
    eng.load_file()
    eng.clean_content()
    eng.calculate_frequency()
    eng.report()
    print()

    # Test TextAnalyzer on Spanish control
    print("Testing TextAnalyzer on Spanish control sample...")
    spa = TextAnalyzer('../data/spanish.txt')
    spa.load_file()
    spa.clean_content()
    spa.calculate_frequency()
    spa.report()
    print()

    # Test CodeAnalyzer on artifact
    print("Testing CodeAnalyzer on mystery artifact...")
    artifact = CodeAnalyzer('../data/artifact.py')
    artifact.load_file()
    artifact.clean_content()
    artifact.calculate_frequency()
    artifact.report()
    print()

    print("Module test complete.")
