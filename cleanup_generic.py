import re

def cleanup(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove templatePattern default value setter in saveSettings
    content = re.sub(r"document\.getElementById\('templatePattern'\)\.value = .*?;\n", "", content)

    # 2. Remove all renderTemplatePersonSelect definitions (there seem to be duplicates)
    content = re.sub(r"\s+renderTemplatePersonSelect\(\) \{[^}]+\},", "", content)

    # 3. Remove applyTemplate method
    content = re.sub(r"\s+applyTemplate\(\) \{[^}]+for \([^)]+\) \{[^}]+\}[^}]+\},", "", content)

    # 4. Remove renderTemplatePersonSelect calls
    content = re.sub(r"\s+this\.renderTemplatePersonSelect\(\);", "", content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    cleanup('scheduler_generic.html')
    cleanup('scheduler_generic_mobile.html')
