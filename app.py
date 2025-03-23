
import ffmpeg

def convert_mp3_to_wav(mp3_file, wav_file=None):
    """
    Converts an MP3 file to WAV format using ffmpeg.
    
    Args:
        mp3_file (str): Path to the input MP3 file.
        wav_file (str, optional): Path to save the WAV file. 
                                  If None, it saves with the same name as input file.
    
    Returns:
        str: Path to the output WAV file.
    """
    if wav_file is None:
        wav_file = mp3_file.replace(".mp3", ".wav")

    try:
        # Use ffmpeg to convert MP3 to WAV
        ffmpeg.input(mp3_file).output(wav_file, format='wav').run(overwrite_output=True, quiet=True)
        return wav_file
    except Exception as e:
        print(f"Error converting {mp3_file} to WAV: {e}")
        return None

# Example usage:
wav_path = convert_mp3_to_wav("file.mp3")
print(f"Converted file saved at: {wav_path}")
