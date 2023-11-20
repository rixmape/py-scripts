"""
This module downloads the audio from a YouTube video and transcribes it using
OpenAI Whisper API.
"""

import argparse
from pytube import YouTube
from pydub import AudioSegment
from openai import OpenAI


def get_args() -> argparse.Namespace:
    """
    Get the command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Transcribe a YouTube video using OpenAI Whisper API."
    )
    parser.add_argument("video_url", type=str, help="URL of the YouTube video.")
    return parser.parse_args()


def get_audio(video_url: str) -> str:
    """
    Download the audio from the YouTube video.

    Args:
        video_url (str): URL of the YouTube video.

    Returns:
        str: Path to the downloaded audio.
    """
    print(f"Downloading audio from {video_url}")
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_path = audio_stream.download()
    print(f"Audio downloaded to {output_path}")
    return output_path


def split_audio(audio_path: str, chunk_length_min: int = 5) -> list[str]:
    """
    Split the audio into 5-minute chunks.

    Args:
        audio_path (str): Path to the audio file.
        chunk_length_min (int): Length of each audio chunk in minutes.

    Returns:
        list[str]: List of paths to the audio chunks.
    """
    print(f"Splitting audio into {chunk_length_min}-minute chunks")
    file_ext = audio_path.split(".")[-1]
    audio = AudioSegment.from_file(audio_path)
    chunk_length_ms = chunk_length_min * 60 * 1000
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunk_path = f"chunk_{i // chunk_length_ms}.{file_ext}"
        chunk.export(chunk_path, format=file_ext)
        chunks.append(chunk_path)
    print(f"Audio split into {len(chunks)} chunks")
    return chunks


def transcribe_audio_chunk(client: OpenAI, audio_chunk_path: str) -> str:
    """
    Transcribe an audio chunk using OpenAI API.

    Args:
        client (OpenAI): OpenAI API client.
        audio_chunk_path (str): Path to the audio chunk.

    Returns:
        str: Transcription of the audio chunk.
    """
    print(f"Transcribing {audio_chunk_path}")
    with open(audio_chunk_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    print(f"Transcription: {transcript.text}")
    return transcript.text


def save_transcript(transcript: str, output_path: str) -> None:
    """
    Save the transcript to a file.

    Args:
        transcript (str): The transcript.
        output_path (str): Path to the output file.
    """
    print(f"Saving transcript to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print("Transcript saved")


if __name__ == "__main__":
    args = get_args()
    audio_path = get_audio(args.video_url)
    audio_chunks = split_audio(audio_path)
    client = OpenAI()
    transcriptions = []

    for audio_chunk in audio_chunks:
        transcriptions.append(transcribe_audio_chunk(client, audio_chunk))

    save_transcript("\n".join(transcriptions), "transcript.txt")
