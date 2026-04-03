import os

base = '/Users/hyuntaeshin/Desktop/JoCoding/folder_1'

# en.html
langs = {
    'en.html': {
        'desktop_marker': '''<div class="nav-item">
                <button class="nav-item-btn">Leaving Job''',
        'desktop_new': '''<div class="nav-item">
                <button class="nav-item-btn">Medical <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="medical-tax.html"><div class="nav-dropdown-dot" style="background:#EC4899;"></div>Medical Tax Deduction</a>
                    <a href="silbi.html"><div class="nav-dropdown-dot" style="background:#06B6D4;"></div>Insurance Calculator</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">Leaving Job''',
        'mobile_marker': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">Leaving Job''',
        'mobile_new': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">Medical</div>
            <a href="medical-tax.html">Medical Tax Deduction</a>
            <a href="silbi.html">Insurance Calculator</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">Leaving Job''',
    },
    'zh.html': {
        'desktop_marker': '''<div class="nav-item">
                <button class="nav-item-btn">离职相关''',
        'desktop_new': '''<div class="nav-item">
                <button class="nav-item-btn">医疗相关 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="medical-tax.html"><div class="nav-dropdown-dot" style="background:#EC4899;"></div>医疗费税额扣除</a>
                    <a href="silbi.html"><div class="nav-dropdown-dot" style="background:#06B6D4;"></div>实费保险计算器</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">离职相关''',
        'mobile_marker': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">离职相关''',
        'mobile_new': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">医疗相关</div>
            <a href="medical-tax.html">医疗费税额扣除</a>
            <a href="silbi.html">实费保险计算器</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">离职相关''',
    },
    'ja.html': {
        'desktop_marker': '''<div class="nav-item">
                <button class="nav-item-btn">退職関連''',
        'desktop_new': '''<div class="nav-item">
                <button class="nav-item-btn">医療関連 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="medical-tax.html"><div class="nav-dropdown-dot" style="background:#EC4899;"></div>医療費税額控除</a>
                    <a href="silbi.html"><div class="nav-dropdown-dot" style="background:#06B6D4;"></div>実費保険計算機</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">退職関連''',
        'mobile_marker': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">退職関連''',
        'mobile_new': '''<div class="nav-mobile-group">
            <div class="nav-mobile-title">医療関連</div>
            <a href="medical-tax.html">医療費税額控除</a>
            <a href="silbi.html">実費保険計算機</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">退職関連''',
    }
}

for fname, cfg in langs.items():
    f = os.path.join(base, fname)
    content = open(f, 'r', encoding='utf-8').read()
    if '医療' in content or 'Medical' in content:
        print(f"⏭  {fname}: 이미 적용됨")
        continue
    content = content.replace(cfg['desktop_marker'], cfg['desktop_new'], 1)
    content = content.replace(cfg['mobile_marker'], cfg['mobile_new'], 1)
    open(f, 'w', encoding='utf-8').write(content)
    print(f"✅ {fname}")

print("완료!")
