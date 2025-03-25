import ffmpeg


def convert_mp3_to_wav(mp3_file, wav_file=None):
    if wav_file is None:
        wav_file = mp3_file.replace(".mp3", ".wav")
    try:
        ffmpeg.input(mp3_file).output(wav_file, format='wav').run(overwrite_output=True, quiet=True)
        return wav_file
    except Exception as e:
        print(f"Error converting {mp3_file} to WAV: {e}")
