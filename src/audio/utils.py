import numpy as np
from moviepy.editor import AudioFileClip


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
