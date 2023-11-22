"""
This module extracts the text from a .srt file.
"""

import argparse
import re


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including path to the .srt
        file.
    """
    parser = argparse.ArgumentParser(
        description="Extract the text from a .srt file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "srt_file_path",
        type=str,
        help="Path to the .srt file.",
    )
    return parser.parse_args()


def extract_subtitle_text(srt_file_path: str) -> str:
    """
    Extracts the text from a .srt file.

    Args:
        srt_file_path (str): Path to the .srt file.

    Returns:
        str: The extracted text.
    """
    with open(srt_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    pattern = re.compile(
        r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n",
        re.DOTALL,  # Allows the dot to match newlines
    )
    matches = pattern.findall(content)
    text = "\n".join(matches)
    return text


if __name__ == "__main__":
    args = get_args()
    text = extract_subtitle_text(args.srt_file_path)
    print(text)
