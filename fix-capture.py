import os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'
files = ['index.html', 'en.html', 'zh.html', 'ja.html']

for fname in files:
    f = os.path.join(base, fname)
    content = open(f, 'r', encoding='utf-8').read()
    original = content
    
    # 1) CSS: captureArea 초기 숨김 추가
    # result-placeholder 정의 뒤에 추가
    content = content.replace(
        '.result-placeholder { background: var(--surface);',
        '#captureArea { display: none; }\n        .result-placeholder { background: var(--surface);'
    )
    
    # 2) JS: calculate() 함수에서 captureArea 보이기 추가
    # resultPlaceholder 숨기는 줄 앞에 추가
    content = content.replace(
        "document.getElementById('resultPlaceholder').style.display = 'none';",
        "document.getElementById('captureArea').style.display = 'block';\n    document.getElementById('resultPlaceholder').style.display = 'none';"
    )
    
    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        print(f"✅ {fname}")
    else:
        print(f"⚠️  {fname}: 변경 없음")

print("\n완료!")
