import whisper

def speech2text(filename, model):
    """
    Args:
        filename (str): Path to an audio file. The file should 
        model (whisper.Model): A model to use for speech recognition.
    Recognize speech in an audio file.
    """
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    print(result.text)
    return result.text