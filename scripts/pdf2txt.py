"""
This module extracts the text from a PDF file.
"""

import argparse
import PyPDF2


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including path to the PDF file
        and path to the output text file.
    """
    parser = argparse.ArgumentParser(
        description="Extract the text from a PDF file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "pdf_path",
        type=str,
        help="Path to the PDF file.",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Path to the output text file.",
    )
    return parser.parse_args()


def pdf_to_text(pdf_path, output_path):
    """
    Converts a PDF file to a text file.

    :param pdf_path: Path to the PDF file to be converted.
    :param output_path: Path where the output text file will be saved.
    """
    try:
        # Open the PDF file
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            # Check if the PDF file is encrypted
            if reader.is_encrypted:
                print("The PDF file is encrypted. Unable to process.")
                return

            # Extract text from each page and write to the output file
            with open(output_path, "w", encoding="utf-8") as text_file:
                for page in reader.pages:
                    text = page.extract_text()
                    text_file.write(text)

        print(f"Text extracted and saved to {output_path}")

    except FileNotFoundError:
        print(f"The file {pdf_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    args = get_args()
    pdf_to_text(args.pdf_path, args.output_path)
