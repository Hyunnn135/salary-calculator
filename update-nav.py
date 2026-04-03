import glob, os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'
html_files = glob.glob(os.path.join(base, '*.html'))

# 새 페이지는 이미 올바른 네비를 갖고 있으므로 제외
skip = ['medical-tax.html', 'silbi.html']

# 데스크톱 네비: "퇴사할 때" 드롭다운 앞에 "병원 갈 때" 삽입
desktop_new = '''            <div class="nav-item">
                <button class="nav-item-btn">병원 갈 때 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="medical-tax.html"><div class="nav-dropdown-dot" style="background:#EC4899;"></div>의료비 세액공제</a>
                    <a href="silbi.html"><div class="nav-dropdown-dot" style="background:#06B6D4;"></div>실비보험 계산기</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">퇴사할 때'''

# 모바일 네비: "퇴사할 때" 그룹 앞에 "병원 갈 때" 삽입
mobile_new = '''        <div class="nav-mobile-group">
            <div class="nav-mobile-title">병원 갈 때</div>
            <a href="medical-tax.html">의료비 세액공제</a>
            <a href="silbi.html">실비보험 계산기</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">퇴사할 때'''

changes = 0
for f in sorted(html_files):
    fname = os.path.basename(f)
    if fname in skip:
        continue
    
    content = open(f, 'r', encoding='utf-8').read()
    original = content
    
    # 이미 "병원 갈 때"가 있으면 스킵
    if '병원 갈 때' in content:
        continue
    
    # 데스크톱 네비 삽입 (퇴사할 때 버튼 앞에)
    # 패턴: </div>\n            <div class="nav-item">\n                <button class="nav-item-btn">퇴사할 때
    desktop_marker = '''<div class="nav-item">
                <button class="nav-item-btn">퇴사할 때'''
    
    if desktop_marker in content:
        content = content.replace(desktop_marker, desktop_new, 1)
    
    # 모바일 네비 삽입
    mobile_marker = '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">퇴사할 때'''
    
    if mobile_marker in content:
        content = content.replace(mobile_marker, mobile_new, 1)
    
    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        print(f"✅ {fname}")
        changes += 1

print(f"\n총 {changes}개 파일 업데이트")
