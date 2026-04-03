import re, glob, os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'
html_files = glob.glob(os.path.join(base, '*.html'))

total_changes = 0
for f in sorted(html_files):
    fname = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    original = content
    
    # Strategy: remove line by line approach for broken comment blocks
    # Pattern 1: ADSENSE-HIDE blocks (greedy, matches everything between start/end markers)
    content = re.sub(
        r'<!-- ADSENSE-HIDE:.*?ADSENSE-HIDE\s*-->\s*',
        '', content, flags=re.DOTALL
    )
    
    # Pattern 2: Any remaining broken ADSENSE-HIDE that lost its end marker
    # (the end --> might have been consumed by nested comment)
    content = re.sub(
        r'<!-- ADSENSE-HIDE:[^\n]*\n.*?(?=\n<!-- ADSENSE-HIDE:|\n<footer|\n<div class="footer|\n<div class="info-card"|\Z)',
        '', content, flags=re.DOTALL
    )
    
    # Pattern 3: Standalone kakao adfit (any wrapper div)
    content = re.sub(
        r'<!--\s*카카오 애드핏\s*-->\s*<div[^>]*>\s*<ins class="kakao_ad_area".*?</div>\s*',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'<div[^>]*>\s*<ins class="kakao_ad_area".*?</div>\s*',
        '', content, flags=re.DOTALL
    )
    
    # Pattern 4: Standalone coupang banner
    content = re.sub(
        r'<!--\s*쿠팡 파트너스[^-]*-->\s*<div class="coupang-banner">.*?</div>\s*',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'<div class="coupang-banner">.*?</div>\s*',
        '', content, flags=re.DOTALL
    )
    
    # Pattern 5: Leftover text fragments
    content = content.replace('ADSENSE-HIDE -->', '')
    content = re.sub(r'<!--\s*ADSENSE-HIDE:[^>]*-->\s*', '', content)
    
    # Clean up multiple blank lines (max 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        
        has_kakao = 'kakao_ad_area' in content
        has_coupang = 'PartnersCoupang' in content or 'coupang-banner' in content
        has_hide = 'ADSENSE-HIDE' in content
        
        issues = []
        if has_kakao: issues.append('카카오 잔존!')
        if has_coupang: issues.append('쿠팡 잔존!')
        if has_hide: issues.append('HIDE태그 잔존!')
        
        status = f" ⚠️ {', '.join(issues)}" if issues else ""
        print(f"✅ {fname}: 정리 완료{status}")
        total_changes += 1
    else:
        has_any = any(x in content for x in ['kakao_ad_area', 'PartnersCoupang', 'ADSENSE-HIDE', 'coupang-banner'])
        if has_any:
            print(f"⚠️  {fname}: 변경 안됨 - 수동 확인 필요")

print(f"\n총 {total_changes}개 파일 수정")

# Final check
print("\n=== 최종 확인 ===")
for f in sorted(html_files):
    fname = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    issues = []
    if 'kakao_ad_area' in content: issues.append('카카오')
    if 'PartnersCoupang' in content: issues.append('쿠팡')
    if 'ADSENSE-HIDE' in content: issues.append('HIDE')
    if 'coupang-banner' in content and fname != 'hide-ads.py': issues.append('쿠팡배너')
    if issues:
        print(f"❌ {fname}: {', '.join(issues)}")

print("완료!")
