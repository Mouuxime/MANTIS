PRONUNCIATION_MAP = {
    "Mantis": "Mantiss",
}


def normalize_tts_text(text: str) -> str:
    for src, dst in PRONUNCIATION_MAP.items():
        text = text.replace(src, dst)
    return text
