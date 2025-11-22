import argparse

import numpy as np
from moviepy.editor import AudioFileClip, VideoClip
from PIL import Image

from utils import load_audio, normalize


def intensity_viz(audio_path, image_path, video_output, fps=30):

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    mono = load_audio(audio_path)
    mono = normalize(mono)

    base_img = Image.open(image_path)
    base_img = np.array(base_img)

    # Function to generate each video frame
    def make_frame(t):
        # Copy the static waveform
        frame = base_img.copy().astype(np.float32)

        idx = int(t/duration*(mono.shape[0]-1))
        val = mono[idx]
        frame *= val

        frame = Image.fromarray(frame.astype(np.uint8), mode="RGB")

        return np.array(frame)

    # Create video clip
    video_clip = VideoClip(make_frame, duration=duration)
    video_clip = video_clip.set_audio(audio_clip)

    # Export
    video_clip.write_videofile(
        video_output,
        fps=fps,
        codec="libx264",
        audio_codec="aac"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Audio color intensity visualizer")

    parser.add_argument("--audio", type=str)
    parser.add_argument("--image", type=str)
    parser.add_argument("--output", type=str)

    args = parser.parse_args()

    intensity_viz(audio_path=args.audio, image_path=args.image,
                  video_output=args.output)
