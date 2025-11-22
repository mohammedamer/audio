import argparse

import numpy as np
from moviepy.editor import AudioFileClip, VideoClip
from PIL import Image


def load_audio(path):

    # Load the audio
    audio_clip = AudioFileClip(path)

    # Convert audio to a numpy array (mono)
    # fps here is only for analysis, not video fps
    analysis_fps = 44100

    # Manually collect chunks into a list, then concatenate
    chunks = list(
        audio_clip.iter_chunks(
            fps=analysis_fps,
            quantize=True,  # get int16-ish PCM
            nbytes=2,
            chunksize=1024
        )
    )

    return np.concatenate(chunks, axis=0).astype(np.float32)


def normalize(audio_array):
    # Convert to mono if stereo
    if audio_array.ndim == 2:
        mono = audio_array.mean(axis=1)
    else:
        mono = audio_array

    min = mono.min()
    max = mono.max()
    return (mono - min)/(max - min + 1e-7)


def main(audio_path, image_path, video_output, fps=30):

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

    main(audio_path=args.audio, image_path=args.image,
         video_output=args.output)
