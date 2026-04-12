#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add "관련 콘텐츠" sections to HTML pages in salarykorea.site
"""

import os
import re
from pathlib import Path

# Calculator metadata
CALCULATORS = {
    'index.html': {
        'title': '연봉 실수령액 계산기',
        'desc': '2026년 기준 연봉별 실수령액을 바로 계산해보세요',
    },
    'salary-table.html': {
        'title': '연봉별 실수령액 표',
        'desc': '2,400만원~2억 연봉별 실수령액을 한눈에 비교',
    },
    'insurance.html': {
        'title': '4대보험 계산기',
        'desc': '내 급여에서 빠지는 4대보험료 정확히 계산',
    },
    'minimum-wage.html': {
        'title': '최저시급 계산기',
        'desc': '2026년 최저시급 기준 일급·주급·월급 계산',
    },
    'holiday-pay.html': {
        'title': '주휴수당 계산기',
        'desc': '주휴수당 포함 실제 받는 금액 계산',
    },
    'retirement.html': {
        'title': '퇴직금 계산기',
        'desc': '근속연수별 퇴직금 예상 금액 계산',
    },
    'unemployment.html': {
        'title': '실업급여 계산기',
        'desc': '실업급여 수급 자격과 예상 금액 확인',
    },
    'income-tax.html': {
        'title': '종합소득세 계산기',
        'desc': '사업·프리랜서 종합소득세 간편 계산',
    },
    'gift-tax.html': {
        'title': '증여세 계산기',
        'desc': '증여 금액별 예상 증여세 계산',
    },
    'acquisition-tax.html': {
        'title': '취득세 계산기',
        'desc': '부동산 취득세 예상 금액 계산',
    },
    'medical-tax.html': {
        'title': '의료비 세액공제 계산기',
        'desc': '연말정산 의료비 공제 예상 금액 계산',
    },
    'silbi.html': {
        'title': '실비보험 계산기',
        'desc': '실비보험 보장 범위와 본인부담금 계산',
    },
    'freelancer-tax.html': {
        'title': '프리랜서 3.3% 계산기',
        'desc': '프리랜서 원천징수 및 환급액 계산',
    },
    'monthly-salary.html': {
        'title': '월급 세후 계산기',
        'desc': '월급 기준 세후 실수령액 계산',
    },
    'entry-salary-ranking.html': {
        'title': '대졸 초봉 순위',
        'desc': '기업별 대졸 초봉 순위 비교',
    },
}

# Guide metadata
GUIDES = {
    'guide-salary.html': '연봉 실수령액 가이드',
    'guide-insurance.html': '4대보험 완벽 가이드',
    'guide-minimum-wage.html': '최저시급 완벽 가이드',
    'guide-holiday-pay.html': '주휴수당 완벽 가이드',
    'guide-retirement.html': '퇴직금 완벽 가이드',
    'guide-unemployment.html': '실업급여 완벽 가이드',
    'guide-income-tax.html': '종합소득세 가이드',
    'guide-medical-tax.html': '의료비 공제 가이드',
    'guide-silbi.html': '실비보험 가이드',
    'guide-freelancer.html': '프리랜서 세금 가이드',
    'tax-guide.html': '연말정산 완벽 가이드',
}

# Company metadata
COMPANIES = {
    'company-samsung.html': '삼성전자',
    'company-hyundai-motor.html': '현대자동차',
    'company-lg-energy.html': 'LG에너지솔루션',
    'company-sk-hynix.html': 'SK하이닉스',
    'company-coupang.html': '쿠팡',
    'company-kakao.html': '카카오',
    'company-naver.html': '네이버',
    'company-posco.html': '포스코',
}

# Salary page metadata
SALARY_PAGES = {
    'salary-2400.html': '연봉 2,400만원',
    'salary-2600.html': '연봉 2,600만원',
    'salary-2800.html': '연봉 2,800만원',
    'salary-3000.html': '연봉 3,000만원',
    'salary-3500.html': '연봉 3,500만원',
    'salary-4000.html': '연봉 4,000만원',
    'salary-4500.html': '연봉 4,500만원',
    'salary-5000.html': '연봉 5,000만원',
    'salary-5500.html': '연봉 5,500만원',
    'salary-6000.html': '연봉 6,000만원',
    'salary-7000.html': '연봉 7,000만원',
    'salary-8000.html': '연봉 8,000만원',
    'salary-9000.html': '연봉 9,000만원',
    'salary-10000.html': '연봉 1억원',
    'salary-15000.html': '연봉 1.5억원',
    'salary-20000.html': '연봉 2억원',
}

# Define relationships
PAGE_CONFIGS = {
    # GROUP 1: Main Calculator Pages
    'index.html': {
        'type': 'calculator',
        'related_calculators': ['salary-table.html', 'insurance.html', 'minimum-wage.html'],
        'related_guides': ['guide-salary.html', 'guide-insurance.html', 'tax-guide.html'],
        'salary_range': ['salary-3000', 'salary-4000', 'salary-5000', 'salary-6000', 'salary-8000', 'salary-10000'],
    },
    'insurance.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'salary-table.html', 'retirement.html'],
        'related_guides': ['guide-insurance.html', 'guide-salary.html'],
        'salary_range': ['salary-3000', 'salary-4000', 'salary-5000'],
    },
    'minimum-wage.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'holiday-pay.html', 'insurance.html'],
        'related_guides': ['guide-minimum-wage.html', 'guide-salary.html'],
    },
    'holiday-pay.html': {
        'type': 'calculator',
        'related_calculators': ['minimum-wage.html', 'index.html', 'insurance.html'],
        'related_guides': ['guide-holiday-pay.html', 'guide-salary.html'],
    },
    'retirement.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'unemployment.html', 'insurance.html'],
        'related_guides': ['guide-retirement.html', 'guide-salary.html'],
    },
    'unemployment.html': {
        'type': 'calculator',
        'related_calculators': ['retirement.html', 'index.html', 'insurance.html'],
        'related_guides': ['guide-unemployment.html', 'guide-salary.html'],
    },
    'income-tax.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'freelancer-tax.html', 'gift-tax.html'],
        'related_guides': ['guide-income-tax.html', 'tax-guide.html'],
    },
    'gift-tax.html': {
        'type': 'calculator',
        'related_calculators': ['acquisition-tax.html', 'income-tax.html', 'index.html'],
        'related_guides': ['tax-guide.html', 'guide-income-tax.html'],
    },
    'acquisition-tax.html': {
        'type': 'calculator',
        'related_calculators': ['gift-tax.html', 'income-tax.html', 'index.html'],
        'related_guides': ['tax-guide.html'],
    },
    'medical-tax.html': {
        'type': 'calculator',
        'related_calculators': ['silbi.html', 'index.html', 'income-tax.html'],
        'related_guides': ['guide-medical-tax.html', 'guide-silbi.html'],
    },
    'silbi.html': {
        'type': 'calculator',
        'related_calculators': ['medical-tax.html', 'insurance.html', 'index.html'],
        'related_guides': ['guide-silbi.html', 'guide-medical-tax.html'],
    },
    'freelancer-tax.html': {
        'type': 'calculator',
        'related_calculators': ['income-tax.html', 'index.html', 'insurance.html'],
        'related_guides': ['guide-freelancer.html', 'tax-guide.html'],
    },
    'monthly-salary.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'salary-table.html', 'insurance.html'],
        'related_guides': ['guide-salary.html'],
    },
    'salary-table.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'insurance.html', 'monthly-salary.html'],
        'related_guides': ['guide-salary.html', 'guide-insurance.html'],
        'salary_range': ['salary-3000', 'salary-4000', 'salary-5000', 'salary-6000', 'salary-8000', 'salary-10000'],
    },
    'entry-salary-ranking.html': {
        'type': 'calculator',
        'related_calculators': ['index.html', 'salary-table.html'],
        'related_guides': ['guide-salary.html'],
    },
}

# Build salary page configs dynamically
salary_levels = [2400, 2600, 2800, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 15000, 20000]
for level in salary_levels:
    filename = f'salary-{level}.html'
    idx = salary_levels.index(level)
    nearby = []
    for offset in [-2, -1, 1, 2]:
        if 0 <= idx + offset < len(salary_levels):
            nearby.append(f"salary-{salary_levels[idx + offset]}.html")

    PAGE_CONFIGS[filename] = {
        'type': 'salary',
        'related_calculators': ['index.html', 'salary-table.html', 'insurance.html'],
        'related_guides': ['guide-salary.html'],
        'related_salaries': nearby,
    }

# Company page configs
for company_file in COMPANIES.keys():
    other_companies = [f for f in COMPANIES.keys() if f != company_file][:4]
    PAGE_CONFIGS[company_file] = {
        'type': 'company',
        'related_companies': other_companies,
        'related_calculators': ['index.html', 'salary-table.html', 'entry-salary-ranking.html'],
    }


def build_calculator_html(filename, title, description):
    return f'''                <a href="{filename}" style="display:flex; align-items:center; gap:14px; padding:14px 16px; background:var(--surface-alt); border-radius:12px; text-decoration:none; transition:all 0.15s;">
                    <div style="width:40px; height:40px; background:var(--accent-light); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="12" y2="14"/></svg>
                    </div>
                    <div>
                        <div style="font-size:0.9rem; font-weight:700; color:var(--text-primary);">{title}</div>
                        <div style="font-size:0.78rem; color:var(--text-secondary); margin-top:2px;">{description}</div>
                    </div>
                </a>
'''

def build_guide_html(filename, title):
    return f'''                <a href="{filename}" style="display:flex; align-items:center; gap:12px; padding:12px 16px; border:1px solid var(--border); border-radius:10px; text-decoration:none; transition:all 0.15s;">
                    <span style="font-size:0.85rem; font-weight:600; color:var(--accent);">→</span>
                    <span style="font-size:0.88rem; font-weight:600; color:var(--text-primary);">{title}</span>
                </a>
'''

def build_salary_tag_html(filename, label):
    return f'                <a href="{filename}" style="padding:8px 16px; background:var(--surface-alt); border:1px solid var(--border); border-radius:8px; font-size:0.82rem; font-weight:600; color:var(--text-primary); text-decoration:none; transition:all 0.15s;">{label}</a>\n'

def build_company_tag_html(filename, label):
    return f'                <a href="{filename}" style="padding:8px 16px; background:var(--surface-alt); border:1px solid var(--border); border-radius:8px; font-size:0.82rem; font-weight:600; color:var(--text-primary); text-decoration:none; transition:all 0.15s;">{label}</a>\n'

def build_related_content_html(page_filename, config):
    html_parts = []

    if 'related_calculators' in config:
        html_parts.append('        <div class="article-card" style="margin-bottom: 24px;">\n            <h2>관련 계산기</h2>\n            <div style="display:grid; gap:12px;">\n')
        for calc_file in config['related_calculators']:
            if calc_file in CALCULATORS:
                meta = CALCULATORS[calc_file]
                html_parts.append(build_calculator_html(calc_file, meta['title'], meta['desc']))
        html_parts.append('            </div>\n        </div>\n\n')

    if 'related_guides' in config:
        html_parts.append('        <div class="article-card" style="margin-bottom: 24px;">\n            <h2>함께 읽으면 좋은 가이드</h2>\n            <div style="display:grid; gap:10px;">\n')
        for guide_file in config['related_guides']:
            if guide_file in GUIDES:
                html_parts.append(build_guide_html(guide_file, GUIDES[guide_file]))
        html_parts.append('            </div>\n        </div>\n\n')

    if 'salary_range' in config:
        html_parts.append('        <div class="article-card" style="margin-bottom: 24px;">\n            <h2>연봉별 실수령액 상세</h2>\n            <div style="display:flex; flex-wrap:wrap; gap:8px;">\n')
        for salary_file_base in config['salary_range']:
            salary_file = f'{salary_file_base}.html'
            if salary_file in SALARY_PAGES:
                html_parts.append(build_salary_tag_html(salary_file, SALARY_PAGES[salary_file]))
        html_parts.append('            </div>\n        </div>\n\n')

    if 'related_salaries' in config:
        html_parts.append('        <div class="article-card" style="margin-bottom: 24px;">\n            <h2>다른 연봉 보기</h2>\n            <div style="display:flex; flex-wrap:wrap; gap:8px;">\n')
        for salary_file in config['related_salaries']:
            if salary_file in SALARY_PAGES:
                html_parts.append(build_salary_tag_html(salary_file, SALARY_PAGES[salary_file]))
        html_parts.append('            </div>\n        </div>\n\n')

    if 'related_companies' in config:
        html_parts.append('        <div class="article-card" style="margin-bottom: 24px;">\n            <h2>다른 기업 연봉 보기</h2>\n            <div style="display:flex; flex-wrap:wrap; gap:8px;">\n')
        for company_file in config['related_companies']:
            if company_file in COMPANIES:
                html_parts.append(build_company_tag_html(company_file, COMPANIES[company_file]))
        html_parts.append('            </div>\n        </div>\n\n')

    return ''.join(html_parts)

def has_related_content(content):
    return bool(re.search(r'관련 계산기|관련 페이지|다른 직종|다른 기업', content))

def is_excluded_page(filename):
    return filename.startswith('guide-') or filename.startswith('job-')

def add_related_content_to_file(filepath):
    filename = os.path.basename(filepath)

    if is_excluded_page(filename):
        return 'skipped', 'Guide or job page (excluded)'

    if filename not in PAGE_CONFIGS:
        return 'skipped', 'No config found'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_related_content(content):
        return 'skipped', 'Already has related content'

    footer_match = re.search(r'<footer\s+class="footer">', content)
    if not footer_match:
        return 'error', 'Footer not found'

    footer_pos = footer_match.start()

    config = PAGE_CONFIGS[filename]
    related_html = build_related_content_html(filename, config)

    new_content = content[:footer_pos] + related_html + content[footer_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return 'modified', f'Added related content ({len(related_html)} bytes)'

def main():
    base_dir = '/sessions/pensive-determined-edison/mnt/folder_1'

    modified = 0
    skipped = 0
    errors = 0

    target_files = set(PAGE_CONFIGS.keys())

    for filename in sorted(target_files):
        filepath = os.path.join(base_dir, filename)

        if not os.path.exists(filepath):
            print(f'SKIP: {filename} (file not found)')
            skipped += 1
            continue

        status, message = add_related_content_to_file(filepath)

        if status == 'modified':
            print(f'✓ {filename}')
            modified += 1
        elif status == 'skipped':
            print(f'- {filename} ({message})')
            skipped += 1
        elif status == 'error':
            print(f'✗ {filename} ({message})')
            errors += 1

    print(f'\n--- SUMMARY ---')
    print(f'Modified: {modified}')
    print(f'Skipped: {skipped}')
    print(f'Errors: {errors}')
    print(f'Total: {modified + skipped + errors}')

if __name__ == '__main__':
    main()
