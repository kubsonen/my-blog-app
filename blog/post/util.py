def cut_text(text, max_len):
    text_len = len(text)
    if text_len > max_len:
        return text[0:max_len] + "..."
    return text
