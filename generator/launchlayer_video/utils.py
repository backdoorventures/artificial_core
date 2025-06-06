import re
from PIL import Image as PILImage, ImageDraw, ImageFont

def split_sentences(text):
    """
    Splits a block of text into sentences using punctuation.
    """
    raw = re.split(r'(?<=[.!?]) +', text.strip())
    return raw if len(raw) > 1 else [text]

def wrap_text(text, font, max_width):
    """
    Wraps text to fit within a max width using the provided font.
    Returns a single string with line breaks.
    """
    words = text.split()
    lines, line = [], ""
    draw = ImageDraw.Draw(PILImage.new("RGB", (10, 10)))
    
    for word in words:
        test = (line + " " + word).strip()
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
        
    return "\n".join(lines)

