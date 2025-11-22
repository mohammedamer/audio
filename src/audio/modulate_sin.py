import argparse

import numpy as np
from moviepy.editor import AudioFileClip, VideoClip
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

from utils import load_audio, normalize


def modulate_sin(audio_path, image_path, video_output,
                 blur=True, wave_color="black", fps=30):

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    mono = load_audio(audio_path)
    mono = normalize(mono)

    base_img = Image.open(image_path)
    if blur:
        base_img = base_img.filter(ImageFilter.GaussianBlur())

    height, width, channels = np.array(base_img).shape

    fig = plt.figure()
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])

    omega = 100/duration

    t_arr = []
    y_arr = []

    # Function to generate each video frame
    def make_frame(t):

        ax.cla()
        ax.imshow(base_img)
        ax.axis("off")

        idx = int(t/duration*(mono.shape[0]-1))
        A = mono[idx]*height/4.

        t = t/duration*width
        y = A*np.sin(omega*t)

        y = height/2. + y

        t_arr.append(t)
        y_arr.append(y)

        ax.plot(t_arr, y_arr, color=wave_color)

        # Render the figure
        fig.tight_layout()
        fig.canvas.draw()

        # RGBA buffer as (H, W, 4)
        buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        w, h = fig.canvas.get_width_height()
        frame = buf.reshape(h, w, channels)[..., :3]

        return frame

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
    parser = argparse.ArgumentParser("Audio modulate sin visualizer")

    parser.add_argument("--audio", type=str)
    parser.add_argument("--image", type=str)
    parser.add_argument("--output", type=str)

    args = parser.parse_args()

    modulate_sin(audio_path=args.audio, image_path=args.image,
                 video_output=args.output)
