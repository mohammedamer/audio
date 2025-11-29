import argparse

import numpy as np
from moviepy.editor import AudioFileClip, VideoClip
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from scipy.fft import fft

from utils import load_audio, normalize


def get_parameters(x, bands):

    X = fft(x)
    X = np.abs(X)

    sample_count = X.shape[0]
    window = max(1, sample_count // bands)

    E_arr = []
    start = 0
    while start < sample_count - 1:
        band = X[start:start+window]

        E = (band**2).sum()
        E_arr.append(E)

        start += window

    E_arr = np.array(E_arr)[2:-2]
    return E_arr / (E_arr.sum() + 1e-7)


def bar_viz(audio_path, image_path, video_output,
            window=16, blur=True, bands=32, color="black", fps=30):

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    mono = load_audio(audio_path)
    mono = normalize(mono)
    mono_padded = np.pad(mono, pad_width=(0, int(window)))

    base_img = Image.open(image_path)
    if blur:
        base_img = base_img.filter(ImageFilter.GaussianBlur())

    height, width = np.array(base_img).shape[0:2]
    dpi = 100

    fig = plt.figure()
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    def make_frame(t):

        ax.cla()

        ax.set_xlim((0, width))
        ax.set_ylim((0, height))

        ax.imshow(base_img)
        ax.invert_yaxis()
        ax.axis("off")

        idx = int(t/duration*(mono.shape[0]-1))
        segment = mono_padded[idx:idx+window]

        params = get_parameters(segment, bands=bands)
        params *= height

        bar_num = len(params)
        bar_width = width/(2*bar_num)
        ax.bar(np.linspace(bar_width, width-bar_width, bar_num),
               params, color=color, width=bar_width)

        # Render the figure
        fig.tight_layout()
        fig.canvas.draw()

        # RGBA buffer as (H, W, 4)
        buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        w, h = fig.canvas.get_width_height()
        frame = buf.reshape(h, w, 4)[..., :3]

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
    parser = argparse.ArgumentParser("Audio bar visualizer")

    parser.add_argument("--audio", type=str)
    parser.add_argument("--image", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--color", type=str, default="black")

    args = parser.parse_args()

    bar_viz(audio_path=args.audio, image_path=args.image,
            video_output=args.output, color=args.color)
