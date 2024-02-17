"""
This module renames all files in a directory using a shortened hash of the file.
"""

import os
import hashlib
import argparse
import logging


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including directory path, character count for hash and flag for enabling logging.
    """
    parser = argparse.ArgumentParser(
        description="Rename files in a directory using a shortened hash of the file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path of the directory.",
    )
    parser.add_argument(
        "--char_count",
        type=int,
        default=10,
        help="Number of characters to use from the hash for the new filenames.",
    )
    parser.add_argument(
        "--enable_logging",
        action="store_true",
        help="Enable logging output.",
    )
    return parser.parse_args()


def setup_logging(enable: bool):
    """
    Set up logging configuration based on the command-line argument.

    Args:
        enable (bool): Flag to enable or disable logging.
    """
    if enable:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


def hash_file(filepath: str, char_count: int) -> str:
    """
    Generate the hash of the file.

    Args:
        filepath (str): Path of the file.
        char_count (int): Number of characters to use from the hash.

    Returns:
        str: Hash of the file.
    """
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()[
        :char_count
    ]  # Return the first char_count characters of the hash


def rename_files(directory: str, char_count: int):
    """
    Rename files in the directory using a shortened hash of the file.

    Args:
        directory (str): Path of the directory.
        char_count (int): Number of characters to use from the hash for the new filenames.
    """
    logging.info("Renaming files in %s", directory)

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = hash_file(filepath, char_count)
            new_filepath = os.path.join(
                dirpath, file_hash + os.path.splitext(filename)[1]
            )
            os.rename(filepath, new_filepath)

    logging.info("Finished renaming files")


if __name__ == "__main__":
    args = get_args()
    setup_logging(args.enable_logging)
    rename_files(args.directory, args.char_count)
