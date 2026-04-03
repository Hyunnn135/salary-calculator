import glob, os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'
html_files = glob.glob(os.path.join(base, '*.html'))

changes = 0
for f in sorted(html_files):
    fname = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    original = content
    
    # Fix .dashboard - add align-items: start
    content = content.replace(
        '.dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }',
        '.dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }'
    )
    
    # Fix .two-col - add align-items: start
    content = content.replace(
        '.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }',
        '.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; align-items: start; }'
    )
    
    # Fix .bottom-grid - add align-items: start
    content = content.replace(
        '.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }',
        '.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; align-items: start; }'
    )
    
    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        print(f"✅ {fname}")
        changes += 1

print(f"\n총 {changes}개 파일 수정")
