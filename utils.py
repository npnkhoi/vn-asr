
import contextlib
import wave


def fix_phone_list(v):
    # Remove empty phones in phone list
    newV = []
    for item in v:
        item = item.strip()
        if not item.isspace() and len(item) > 0:
            newV.append(item)
    return newV

def get_audio_length(audio_filename: str) -> float:
    with contextlib.closing(wave.open(audio_filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration