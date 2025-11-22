import argparse

from moviepy.editor import VideoFileClip


def main(video_path, audio_output):

    # Load video
    with VideoFileClip(video_path) as clip:

        # Write audio to a file (format inferred from extension)
        clip.audio.write_audiofile(audio_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Video 2 Audio")

    parser.add_argument("--video", type=str)
    parser.add_argument("--output", type=str)

    args = parser.parse_args()

    main(video_path=args.video, audio_output=args.output)
