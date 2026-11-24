import re
import markdown

def format_manuscript(text):
    # Step 1: Extract sidenotes and replace them with placeholders
    sidenotes = []

    def extract_sidenote(match):
        sidenotes.append(match.group(1))
        return f"SIDENOTEPLACEHOLDER{sidenotes.__len__() - 1}END"

    text = re.sub(r'\(\((.*?)\)\)', extract_sidenote, text)

    # Step 2: Convert Markdown to HTML
    html = markdown.markdown(text, extensions=['tables'])
    
    # Step 3: Restore sidenotes
    for i, note in enumerate(sidenotes):
        sidenote_html = f'<span class="sidenote-number" tabindex="0"><small class="sidenote">{note}</small></span>'
        html = html.replace(f"SIDENOTEPLACEHOLDER{i}END", sidenote_html)

    #Step 4: Wrap the result in a complete HTML document
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Red Wave That Wasn't</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
{html}
</body>
</html>
"""
    return document

# Read manuscript
with open("draft.md","r",encoding="utf-8") as f:
    manuscript = f.read()

#Convert manuscript
html = format_manuscript(manuscript)

#Write output
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)