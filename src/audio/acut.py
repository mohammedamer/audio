import argparse

from moviepy.editor import AudioFileClip, AudioClip


def hhmmss_to_seconds(t: str) -> float:
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main(audio_path, output_path, start, end):

    if start is None:
        start = 0
    else:
        start = hhmmss_to_seconds(start)

    end = hhmmss_to_seconds(end)

    with AudioFileClip(audio_path) as audio:
        audio: AudioClip = audio.subclip(start, end)
        audio.write_audiofile(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Audio cut")

    parser.add_argument("--audio", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--start", type=str, default=None)
    parser.add_argument("--end", type=str)

    args = parser.parse_args()

    main(audio_path=args.audio, output_path=args.output,
         start=args.start, end=args.end)
