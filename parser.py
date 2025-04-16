import re

def clean_text(text):
    lines = text.splitlines()
    skip = ['copy', 'edit', 'view raw', 'bash', 'CopyEdit']
    return "\n".join(line for line in lines if not any(k in line.lower() for k in skip))

def extract_code_blocks(text):
    return re.findall(r"```(?:[\w+]*\n)?(.*?)```", text, re.DOTALL)

def smart_summarize(text):
    cleaned = clean_text(text)
    messages = []
    speaker = "AI"

    # Detect speaker and organize messages
    for line in cleaned.splitlines():
        if line.strip().startswith("You:"):
            speaker = "You"
            content = line.replace("You:", "").strip()
        elif line.strip().startswith("AI:") or line.strip().startswith("Assistant:"):
            speaker = "AI"
            content = line.replace("AI:", "").replace("Assistant:", "").strip()
        else:
            content = line.strip()

        if content:
            messages.append((speaker, content))

    # Group and format logically
    structured = ""
    steps = []
    step_num = 1
    current_step = []

    for i, (speaker, content) in enumerate(messages):
        if speaker == "AI" and ("step" in content.lower() or "first" in content.lower()):
            if current_step:
                steps.append(current_step)
                current_step = []
            current_step.append((speaker, content))
        elif speaker == "You" and "?" in content:
            current_step.append((speaker, content))
        else:
            current_step.append((speaker, content))

    if current_step:
        steps.append(current_step)

    for idx, step in enumerate(steps):
        structured += f"<h4>🔹 Step {idx+1}</h4>\n"
        for spk, line in step:
            role = "You" if spk == "You" else "AI"
            color_class = "speaker-you" if spk == "You" else "speaker-ai"
            structured += f"<div class='{color_class}'><b>{role}:</b> <span class='step-text'>{line}</span></div>\n"

    code_blocks = extract_code_blocks(cleaned)
    return structured, cleaned, code_blocks
