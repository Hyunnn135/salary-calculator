import re, glob, os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'
html_files = glob.glob(os.path.join(base, '*.html'))

# Patterns to remove (covers both commented and uncommented versions)
patterns = [
    # 1) Broken ADSENSE-HIDE comment block for kakao
    re.compile(
        r'<!-- ADSENSE-HIDE: 카카오 애드핏.*?ADSENSE-HIDE -->\s*',
        re.DOTALL
    ),
    # 2) Broken ADSENSE-HIDE comment block for coupang
    re.compile(
        r'<!-- ADSENSE-HIDE: 쿠팡 파트너스.*?ADSENSE-HIDE -->\s*',
        re.DOTALL
    ),
    # 3) Uncommented kakao adfit block (for index.html etc)
    re.compile(
        r'<!-- 카카오 애드핏 -->\s*<div style="text-align:center;[^"]*">\s*<ins class="kakao_ad_area".*?</div>\s*',
        re.DOTALL
    ),
    # 4) Uncommented coupang banner block
    re.compile(
        r'<!-- 쿠팡 파트너스 배너 -->\s*<div class="coupang-banner">.*?</div>\s*',
        re.DOTALL
    ),
    # 5) Coupang banner without comment header
    re.compile(
        r'<div class="coupang-banner">\s*<script src="https://ads-partners\.coupang\.com.*?</div>\s*',
        re.DOTALL
    ),
    # 6) Standalone kakao adfit (no comment header)
    re.compile(
        r'<div style="text-align:center;[^"]*">\s*<ins class="kakao_ad_area".*?</div>\s*',
        re.DOTALL
    ),
]

total_changes = 0
for f in sorted(html_files):
    fname = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    original = content
    
    for pat in patterns:
        content = pat.sub('', content)
    
    # Also clean up any leftover "ADSENSE-HIDE -->" text that might be visible
    content = content.replace('ADSENSE-HIDE -->', '')
    
    if content != original:
        # Count removals
        removed_kakao = 'kakao_ad_area' not in content and 'kakao_ad_area' in original
        removed_coupang = 'PartnersCoupang' not in content and 'PartnersCoupang' in original
        
        open(f, 'w', encoding='utf-8').write(content)
        parts = []
        if removed_kakao: parts.append('카카오')
        if removed_coupang: parts.append('쿠팡')
        print(f"✅ {fname}: {' + '.join(parts) if parts else '정리'} 제거")
        total_changes += 1
    else:
        # Check if ads still remain
        has_kakao = 'kakao_ad_area' in content
        has_coupang = 'PartnersCoupang' in content
        if has_kakao or has_coupang:
            print(f"⚠️  {fname}: 광고 잔존 (kakao={has_kakao}, coupang={has_coupang})")
        
print(f"\n총 {total_changes}개 파일 수정")
