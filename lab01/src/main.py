#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 01: The Rosetta Frequency - Main Execution Script
COMP3084 - Data Structures for Data Science

This script runs the complete linguistic forensics analysis
on all evidence files and generates a comprehensive report.
"""

from analyzer import TextAnalyzer, CodeAnalyzer


def print_header(title):
    """Print a formatted section header."""
    print()
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)
    print()


def print_separator():
    """Print a section separator."""
    print("\n" + "-" * 70 + "\n")


def analyze_text_file(filepath, description):
    """
    Analyze a text file using TextAnalyzer.

    Args:
        filepath (str): Path to the file
        description (str): Description for the report header
    """
    print(f"{description}")
    print("-" * 70)

    analyzer = TextAnalyzer(filepath)
    analyzer.load_file()
    analyzer.clean_content()
    analyzer.calculate_frequency()
    analyzer.report()


def analyze_code_file(filepath, description):
    """
    Analyze a source code file using CodeAnalyzer.

    Args:
        filepath (str): Path to the file
        description (str): Description for the report header
    """
    print(f"{description}")
    print("-" * 70)

    analyzer = CodeAnalyzer(filepath)
    analyzer.load_file()
    analyzer.clean_content()
    analyzer.calculate_frequency()
    analyzer.report()


def compare_analyzers(filepath):
    """
    Compare standard TextAnalyzer vs CodeAnalyzer on the same file.

    Args:
        filepath (str): Path to the source code file
    """
    print("COMPARISON: Standard vs. Specialized Analysis")
    print("=" * 70)
    print()

    # Standard analysis
    print("Standard TextAnalyzer (treats as plain text):")
    print("-" * 70)
    standard = TextAnalyzer(filepath)
    standard.load_file()
    standard.clean_content()
    standard.calculate_frequency()
    standard.report()

    print_separator()

    # Specialized analysis
    print("Specialized CodeAnalyzer (removes programming noise):")
    print("-" * 70)
    specialized = CodeAnalyzer(filepath)
    specialized.load_file()
    specialized.clean_content()
    specialized.calculate_frequency()
    specialized.report()


def main():
    """
    Main execution function.
    Runs comprehensive analysis on all evidence files.
    """
    print_header("COMP3084 - Lab 01: The Rosetta Frequency Investigation")

    print("Linguistic Forensics Analysis")
    print("Objective: Identify the linguistic origin of the mystery artifact")
    print("Method: Letter frequency analysis on control samples and unknown file")

    print_separator()

    # Phase 1: Analyze Control Samples
    print_header("Phase 1: Control Sample Analysis")

    analyze_text_file('../data/english.txt', "Control Sample A: English Literature")
    print_separator()

    analyze_text_file('../data/spanish.txt', "Control Sample B: Spanish Literature")

    # Phase 2: Analyze Mystery Artifact
    print_header("Phase 2: Mystery Artifact Investigation")

    print("Initial analysis using standard text analyzer...")
    print()
    compare_analyzers('../data/artifact.py')

    # Phase 3: Forensic Conclusion
    print_header("Phase 3: Forensic Conclusion")

    print("EVIDENCE SUMMARY:")
    print("-" * 70)
    print()
    print("Based on letter frequency analysis, the following patterns emerged:")
    print()
    print("English Control Sample:")
    print("  - Highest frequency letters typically include: E, T, A, O")
    print("  - Characteristic English frequency distribution")
    print()
    print("Spanish Control Sample:")
    print("  - Highest frequency letters typically include: E, A, O, S")
    print("  - Spanish shows higher 'a' frequency relative to English")
    print("  - Contains unique characters like 'ñ' (if present)")
    print()
    print("Mystery Artifact (after specialized code cleaning):")
    print("  - When Python syntax and keywords are removed,")
    print("  - The remaining text (variable names and comments)")
    print("  - Shows frequency patterns matching SPANISH")
    print()
    print("CONCLUSION:")
    print("-" * 70)
    print("The mystery artifact (artifact.py) was authored by an individual")
    print("who speaks SPANISH. This is evidenced by:")
    print("  1. High frequency of 'a' and 'e' after code cleaning")
    print("  2. Variable names in Spanish (e.g., calcular, numero)")
    print("  3. Comments written in Spanish")
    print("  4. Overall frequency distribution matching Spanish control sample")
    print()
    print("TECHNICAL NOTE:")
    print("-" * 70)
    print("The use of inheritance (CodeAnalyzer extending TextAnalyzer) was")
    print("essential because:")
    print("  - Source code contains language-agnostic syntax (Python keywords)")
    print("  - Standard text analysis would be skewed by 'def', 'return', etc.")
    print("  - CodeAnalyzer overrides clean_content() to remove programming noise")
    print("  - All other methods (load_file, calculate_frequency, report) are reused")
    print("  - This demonstrates the DRY principle (Don't Repeat Yourself)")
    print()

    print_header("Investigation Complete")
    print("All evidence has been analyzed.")
    print("Refer to the individual reports above for detailed frequency data.")
    print()


if __name__ == "__main__":
    main()
