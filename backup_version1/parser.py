import re

def clean_text(text):
    lines = text.splitlines()
    skip_keywords = ['copy', 'edit', 'view raw', 'bash']
    filtered = []

    for line in lines:
        if any(k in line.lower() for k in skip_keywords):
            continue
        filtered.append(line)

    return "\n".join(filtered)

def extract_code_blocks(text):
    return re.findall(r"```(?:[\w+]*\n)?(.*?)```", text, re.DOTALL)

def summarize(text):
    cleaned = clean_text(text)
    return cleaned[:3000] + ("\n...\n" if len(cleaned) > 3000 else "")
