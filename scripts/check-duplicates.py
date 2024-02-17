"""
This module identifies and lists down all duplicate files in a directory using hashing.
"""

import os
import hashlib
import argparse
import logging


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including directory path and flag for enabling logging.
    """
    parser = argparse.ArgumentParser(
        description="Identify duplicate files in a directory using hashing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path of the directory.",
    )
    parser.add_argument(
        "--enable_logging",
        action="store_true",
        help="Enable logging output.",
    )
    return parser.parse_args()


def hash_file(filepath: str) -> str:
    """
    Generate the hash of the file.

    Args:
        filepath (str): Path of the file.

    Returns:
        str: Hash of the file.
    """
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()


def find_duplicates(directory: str) -> list[tuple[str, str]]:
    """
    Identify duplicate files in the directory.

    Args:
        directory (str): Path of the directory.

    Returns:
        list[tuple[str, str]]: List of tuples where each tuple contains the path of the duplicate file and the original file.
    """
    logging.info("Identifying duplicate files in %s", directory)
    file_hashes = {}
    duplicates = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = hash_file(filepath)
            if file_hash in file_hashes:
                duplicates.append((filepath, file_hashes[file_hash]))
            else:
                file_hashes[file_hash] = filepath

    logging.info("Identified %d duplicate files", len(duplicates))
    return duplicates


def print_duplicates(duplicates: list[tuple[str, str]]):
    """
    Print the duplicate files.

    Args:
        duplicates (list[tuple[str, str]]): List of tuples where each tuple contains the path of the duplicate file and the original file.
    """
    logging.info("Printing duplicate files")
    if duplicates:
        for dup in duplicates:
            print(f"{dup[0]} is a duplicate of {dup[1]}")
    else:
        print("No duplicate files found.")


if __name__ == "__main__":
    args = get_args()

    if args.enable_logging:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    duplicates = find_duplicates(args.directory)
    print_duplicates(duplicates)
