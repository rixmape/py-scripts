"""
This module downloads the audio from a YouTube video and transcribes it using
OpenAI Whisper API.
"""

import argparse
import logging
import os
from pytube import YouTube
from pydub import AudioSegment
from openai import OpenAI


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments including video URL, flag for
        keeping audio files, and flag for enabling logging.
    """
    parser = argparse.ArgumentParser(
        description="Transcribe a YouTube video using OpenAI Whisper API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "video_url",
        type=str,
        help="URL of the YouTube video.",
    )
    parser.add_argument(
        "--keep_audio",
        action="store_true",
        help="Keep audio files after transcription.",
    )
    parser.add_argument(
        "--enable_logging",
        action="store_true",
        help="Enable logging output.",
    )
    return parser.parse_args()


def get_audio(video_url: str) -> str:
    """
    Download the audio from the YouTube video.

    Args:
        video_url (str): URL of the YouTube video.

    Returns:
        str: Path to the downloaded audio file.
    """
    logging.info("Downloading audio from %s", video_url)
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_path = audio_stream.download()
    logging.info("Audio downloaded to %s", output_path)
    return output_path


def split_audio(audio_path: str, chunk_length_min: int = 5) -> list[str]:
    """
    Split the audio into chunks of a specified length.

    Args:
        audio_path (str): Path to the audio file.
        chunk_length_min (int): Length of each audio chunk in minutes. Default is 5 minutes.

    Returns:
        list[str]: List of paths to the audio chunks.
    """
    logging.info("Splitting audio into %s-minute chunks", chunk_length_min)
    file_ext = audio_path.split(".")[-1]
    audio = AudioSegment.from_file(audio_path)
    chunk_length_ms = chunk_length_min * 60 * 1000
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunk_path = f"chunk_{i // chunk_length_ms}.{file_ext}"
        chunk.export(chunk_path, format=file_ext)
        chunks.append(chunk_path)
    logging.info("Audio split into %d chunks", len(chunks))
    return chunks


def transcribe_audio_chunks(client: OpenAI, audio_chunks: list[str]) -> str:
    """
    Transcribe all audio chunks using OpenAI API and return the combined transcription.

    Args:
        client (OpenAI): OpenAI API client.
        audio_chunks (list[str]): List of paths to the audio chunks.

    Returns:
        str: Combined transcription of all audio chunks.
    """
    transcriptions = []
    for audio_chunk in audio_chunks:
        logging.info("Transcribing %s", audio_chunk)
        with open(audio_chunk, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        logging.info("Transcription obtained")
        transcriptions.append(transcript.text)
    return "\n".join(transcriptions)


def save_transcript(transcript: str, output_path: str) -> None:
    """
    Save the transcript to a file.

    Args:
        transcript (str): The combined transcript.
        output_path (str): Path to the output file.
    """
    logging.info("Saving transcript to %s", output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    logging.info("Transcript saved")


def cleanup_audio_files(audio_chunks: list[str], keep_audio: bool):
    """
    Delete audio chunk files unless the keep_audio flag is set.

    Args:
        audio_chunks (list[str]): List of audio chunk file paths.
        keep_audio (bool): Flag indicating whether to keep audio files after transcription.
    """
    if not keep_audio:
        for audio_chunk in audio_chunks:
            os.remove(audio_chunk)
        logging.info("Audio chunk files deleted.")


if __name__ == "__main__":
    args = get_args()

    if args.enable_logging:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    audio_path = get_audio(args.video_url)
    audio_chunks = split_audio(audio_path)
    client = OpenAI()
    transcript = transcribe_audio_chunks(client, audio_chunks)
    save_transcript(transcript, "transcript.txt")
    cleanup_audio_files(audio_chunks, args.keep_audio)
