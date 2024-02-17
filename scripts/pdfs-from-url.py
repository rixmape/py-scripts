"""
This module downloads all PDF files from a given URL.
"""

import os
import argparse
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including the URL to download PDFs from and the output path.
    """
    parser = argparse.ArgumentParser(
        description="Download all PDF files from a given URL.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "url",
        type=str,
        help="The URL to download PDFs from.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=".",
        help="The directory to save the PDF files.",
    )
    parser.add_argument(
        "--enable_logging",
        action="store_true",
        help="Enable logging output.",
    )
    return parser.parse_args()


def download_pdf(url: str, output_path: str):
    """
    Download a PDF file from a URL.

    Args:
        url (str): The URL of the PDF file.
        output_path (str): The path to save the PDF file.
    """
    logging.info(f"Downloading %s", url)
    response = requests.get(url)
    with open(output_path, "wb") as output_file:
        output_file.write(response.content)
    logging.info(f"PDF saved to %s", output_path)


def download_all_pdfs(url: str, output_dir: str):
    """
    Download all PDF files from a given URL.

    Args:
        url (str): The URL to download PDFs from.
        output_dir (str): The directory to save the PDF files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.select("a[href$='.pdf']"):
        pdf_url = urljoin(url, link["href"])
        output_path = os.path.join(output_dir, os.path.basename(pdf_url))
        download_pdf(pdf_url, output_path)


if __name__ == "__main__":
    args = get_args()

    if args.enable_logging:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    download_all_pdfs(args.url, args.output)
