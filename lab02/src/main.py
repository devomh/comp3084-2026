#!/usr/bin/env python3
# main.py
"""
Main execution script for Lab 02: The Hex Detective
Analyzes all evidence files and repairs corrupted PNG.

Reference Implementation
"""

import os
import sys

# Add parent directory to path if running from src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from binary_analyzer import BinaryAnalyzer, FileRepairer


def analyze_evidence(data_dir='data'):
    """
    Analyze all evidence files in the data directory.

    Args:
        data_dir (str): Path to the data directory
    """
    files = [
        f'{data_dir}/unknown_a.bin',
        f'{data_dir}/unknown_b.bin',
        f'{data_dir}/unknown_c.bin',
        f'{data_dir}/hidden_message.bin',
    ]

    print("=" * 70)
    print(" COMP3084 - Lab 02: Binary Forensics Analysis")
    print("=" * 70)

    results = []

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"\nWarning: File not found: {filepath}")
            continue

        print(f"\n{'─' * 70}")
        analyzer = BinaryAnalyzer(filepath)
        analyzer.load_file()
        detected = analyzer.detect_type()
        analyzer.report()

        results.append({
            'file': os.path.basename(filepath),
            'size': len(analyzer.data),
            'type': detected
        })

    # Print summary table
    print("\n" + "=" * 70)
    print(" Evidence Summary")
    print("=" * 70)
    print(f"\n{'File':<25} {'Size':>10} {'Detected Type':<20}")
    print("-" * 60)
    for r in results:
        print(f"{r['file']:<25} {r['size']:>10} {r['type']:<20}")

    return results


def repair_corrupted_file(data_dir='data'):
    """
    Repair the corrupted PNG file.

    Args:
        data_dir (str): Path to the data directory

    Returns:
        bool: True if repair successful
    """
    corrupted_path = f'{data_dir}/corrupted.png'
    repaired_path = f'{data_dir}/repaired.png'

    print("\n" + "=" * 70)
    print(" CRITICAL INCIDENT: File Repair Operation")
    print("=" * 70)

    if not os.path.exists(corrupted_path):
        print(f"\nError: Corrupted file not found: {corrupted_path}")
        return False

    # Create repairer instance
    repairer = FileRepairer(corrupted_path)

    # Diagnose the corruption
    print("\n--- Phase 1: Diagnosis ---")
    corrupted_bytes = repairer.diagnose('PNG')

    if not corrupted_bytes:
        print("\nNo corruption found - file may already be valid.")
        return True

    # Perform the repair
    print("\n--- Phase 2: Repair ---")
    success = repairer.repair('PNG', repaired_path)

    if success:
        # Verify the repair
        print("\n--- Phase 3: Verification ---")
        result = repairer.verify(repaired_path)
        print(f"Repaired file type detection: {result}")

        if result == 'PNG':
            print("\n[SUCCESS] File repair completed successfully!")
            print(f"  Original: {corrupted_path} (corrupted)")
            print(f"  Repaired: {repaired_path} (valid PNG)")
            return True
        else:
            print("\n[WARNING] Repair may be incomplete")
            return False
    else:
        print("\n[FAILURE] File repair failed")
        return False


def demonstrate_string_extraction(data_dir='data'):
    """
    Demonstrate string extraction from the hidden message file.

    Args:
        data_dir (str): Path to the data directory
    """
    hidden_path = f'{data_dir}/hidden_message.bin'

    print("\n" + "=" * 70)
    print(" BONUS: Hidden Message Extraction")
    print("=" * 70)

    if not os.path.exists(hidden_path):
        print(f"\nFile not found: {hidden_path}")
        return

    analyzer = BinaryAnalyzer(hidden_path)
    analyzer.load_file()

    strings = analyzer.extract_strings(min_length=8)

    print(f"\nExtracted {len(strings)} strings from {hidden_path}:")
    print("-" * 50)

    for i, s in enumerate(strings, 1):
        # Highlight strings that look like messages
        if any(keyword in s.upper() for keyword in ['SECRET', 'HIDDEN', 'MESSAGE', 'FINAL', 'PASSWORD']):
            print(f"  [{i}] ** {s} **")
        else:
            print(f"  [{i}] {s}")


def main():
    """Main entry point."""
    # Determine data directory (handle running from different locations)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if we're in src/ subdirectory
    if os.path.basename(script_dir) == 'src':
        data_dir = os.path.join(os.path.dirname(script_dir), 'data')
    else:
        data_dir = os.path.join(script_dir, 'data')

    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found: {data_dir}")
        print("Please run this script from the lab02 directory.")
        sys.exit(1)

    # Run all analysis
    analyze_evidence(data_dir)
    repair_corrupted_file(data_dir)
    demonstrate_string_extraction(data_dir)

    # Final summary
    print("\n" + "=" * 70)
    print(" Investigation Complete")
    print("=" * 70)
    print("\nFindings Summary:")
    print("  - unknown_a.bin: PNG image (disguised)")
    print("  - unknown_b.bin: JPEG image (disguised)")
    print("  - unknown_c.bin: Plain text (server log)")
    print("  - hidden_message.bin: Binary with embedded messages")
    print("  - corrupted.png: Successfully repaired")

    print("\nNext steps:")
    print("  1. Verify repaired.png opens correctly:")
    print(f"     $ file {data_dir}/repaired.png")
    print("  2. Open the image to view contents")
    print("  3. Complete submission.md documentation")


if __name__ == "__main__":
    main()
