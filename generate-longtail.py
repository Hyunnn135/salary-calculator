#!/usr/bin/env python3
"""
월급연구소 - 직종별/기업별 롱테일 SEO 페이지 자동 생성기
사용법: python3 generate-longtail.py
"""

import os, json, math

# ── 2026년 4대보험 요율 ──
NP_RATE = 0.045       # 국민연금
HI_RATE = 0.03545     # 건강보험
LTC_RATE = 0.1295     # 장기요양 (건보의 %)
EI_RATE = 0.009       # 고용보험
NP_MAX = 590_000      # 국민연금 상한 (월 기준소득월액 상한 약 590만원 기준)

# ── 간이세액표 근사 (부양가족 1인 기준) ──
SIMPLE_TAX = [
    (1_060_000, 0),
    (1_500_000, 12_150),
    (2_000_000, 21_060),
    (2_500_000, 31_784),
    (3_000_000, 55_790),
    (3_500_000, 84_180),
    (4_000_000, 113_590),
    (5_000_000, 184_170),
    (6_000_000, 262_230),
    (7_000_000, 348_870),
    (8_000_000, 445_780),
    (10_000_000, 676_910),
    (14_000_000, 1_258_160),
    (20_000_000, 2_190_000),
]

def get_income_tax(monthly):
    """간이세액표 보간으로 소득세 추정"""
    if monthly <= SIMPLE_TAX[0][0]:
        return 0
    for i in range(1, len(SIMPLE_TAX)):
        if monthly <= SIMPLE_TAX[i][0]:
            low_m, low_t = SIMPLE_TAX[i-1]
            high_m, high_t = SIMPLE_TAX[i]
            ratio = (monthly - low_m) / (high_m - low_m)
            return int(low_t + (high_t - low_t) * ratio)
    return int(SIMPLE_TAX[-1][1] * (monthly / SIMPLE_TAX[-1][0]))

def calc_salary(annual):
    """연봉 → 실수령액 계산"""
    monthly = annual / 12
    np = min(int(monthly * NP_RATE), NP_MAX)
    hi = int(monthly * HI_RATE)
    ltc = int(hi * LTC_RATE)
    ei = int(monthly * EI_RATE)
    tax = get_income_tax(monthly)
    local_tax = int(tax * 0.1)
    total_ded = np + hi + ltc + ei + tax + local_tax
    net = int(monthly) - total_ded
    return {
        'annual': annual,
        'monthly': int(monthly),
        'np': np, 'hi': hi, 'ltc': ltc, 'ei': ei,
        'tax': tax, 'local_tax': local_tax,
        'total_ded': total_ded, 'net': net,
        'annual_net': net * 12,
        'ded_rate': round(total_ded / monthly * 100, 1)
    }

def fmt(n):
    """숫자 포맷 (천 단위 콤마)"""
    return f"{n:,}"

def fmt_man(n):
    """만원 단위 포맷"""
    if n >= 10000:
        return f"{n//10000}억{' ' + str(n%10000) + '만' if n%10000 else ''}원"
    return f"{n:,}만원"

# ── 직종별 데이터 ──
JOBS = [
    # (slug, 직종명, 설명, 연봉 목록 [신입, 경력3년, 경력7년, 경력10년+], 특이사항)
    {
        'slug': 'nurse', 'name': '간호사',
        'desc': '병원에서 근무하는 간호사의 연봉과 실수령액을 경력별로 정리했습니다.',
        'keyword': '간호사 연봉',
        'salaries': [('신입 (1년차)', 3200), ('경력 3년차', 3800), ('경력 5년차', 4500), ('경력 10년차', 5500), ('수간호사', 6500)],
        'info': '간호사는 3교대 근무에 따른 야간수당, 위험수당 등이 추가되어 실제 수령액은 기본급보다 높을 수 있습니다. 대학병원은 중소병원 대비 10~20% 높은 급여를 제공하며, 전문간호사 자격 취득 시 추가 수당이 발생합니다.',
        'tip': '야간근무수당은 통상임금의 50%가 가산됩니다. 비과세 식대(월 20만원)를 적용하면 실수령액이 더 올라갑니다.'
    },
    {
        'slug': 'teacher', 'name': '교사',
        'desc': '초·중·고 교사의 호봉별 연봉과 실수령액을 정리했습니다.',
        'keyword': '교사 연봉',
        'salaries': [('신규임용 (1호봉)', 3200), ('5호봉 (5년차)', 3800), ('10호봉 (10년차)', 4600), ('20호봉 (20년차)', 6200), ('30호봉 (30년차)', 7800)],
        'info': '교사는 공무원 봉급표에 따라 호봉이 매년 올라갑니다. 기본급 외에 담임수당, 보직수당, 정근수당(연 2회) 등이 추가되며, 방학 중에도 급여가 동일하게 지급됩니다. 사립학교 교사도 공무원 봉급표를 준용합니다.',
        'tip': '교사는 명절 성과급, 정근수당 등으로 실제 연간 수입이 봉급표보다 15~20% 높습니다.'
    },
    {
        'slug': 'police', 'name': '경찰',
        'desc': '경찰공무원의 계급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '경찰 연봉',
        'salaries': [('순경 (신임)', 3000), ('경장 (4년차)', 3500), ('경사 (8년차)', 4200), ('경위 (15년차)', 5200), ('경감 (20년차)', 6500)],
        'info': '경찰은 일반 공무원 대비 약 11% 높은 공안직 봉급을 적용받습니다. 야간근무수당, 위험근무수당, 초과근무수당 등이 기본급에 추가됩니다. 특히 형사·교통 등 현장 부서는 초과근무수당이 상당합니다.',
        'tip': '경찰 초과근무수당은 월 최대 57시간까지 인정되며, 이를 포함하면 실제 월 수령액은 기본급 대비 30~50% 높아질 수 있습니다.'
    },
    {
        'slug': 'firefighter', 'name': '소방관',
        'desc': '소방공무원의 계급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '소방관 연봉',
        'salaries': [('소방사 (신임)', 3000), ('소방교 (5년차)', 3600), ('소방장 (10년차)', 4300), ('소방위 (15년차)', 5200), ('소방경 (20년차)', 6200)],
        'info': '소방관은 공안직 봉급표를 적용받아 일반 공무원보다 11% 높은 기본급을 받습니다. 24시간 교대근무에 따른 야간근무수당, 위험근무수당이 추가되며, 화재·구조 출동 시 특수근무수당도 지급됩니다.',
        'tip': '소방관은 위험직군으로 분류되어 퇴직 시 위험직무수당 가산금이 추가됩니다.'
    },
    {
        'slug': 'civil-servant-9', 'name': '공무원 9급',
        'desc': '일반직 공무원 9급의 호봉별 연봉과 실수령액을 정리했습니다.',
        'keyword': '공무원 9급 연봉',
        'salaries': [('1호봉 (신규)', 2500), ('5호봉 (5년차)', 2900), ('10호봉 (10년차)', 3500), ('15호봉 (15년차)', 4000), ('20호봉 (20년차)', 4500)],
        'info': '9급 공무원은 가장 낮은 직급이지만, 매년 호봉 승급으로 꾸준히 급여가 올라갑니다. 정근수당(근속 연수에 따라 월봉의 0~50%), 가족수당, 직급보조비 등이 추가됩니다. 5년 이상 근무 시 연봉 상승 폭이 눈에 띄게 커집니다.',
        'tip': '공무원 연금(기여금 9%)은 4대보험 국민연금 대신 납부하며, 퇴직 후 연금 수령이 가능합니다. 9급 20년 근속 시 월 100만원 이상의 연금을 받을 수 있습니다.'
    },
    {
        'slug': 'civil-servant-7', 'name': '공무원 7급',
        'desc': '일반직 공무원 7급의 호봉별 연봉과 실수령액을 정리했습니다.',
        'keyword': '공무원 7급 연봉',
        'salaries': [('1호봉 (신규)', 3000), ('5호봉 (5년차)', 3500), ('10호봉 (10년차)', 4200), ('15호봉 (15년차)', 5000), ('20호봉 (20년차)', 5700)],
        'info': '7급 공무원은 행정 실무의 중추적 역할을 담당합니다. 9급 대비 직급보조비가 높고, 승진 속도도 빠릅니다. 중앙부처 근무 시 특수지 근무수당이 추가되며, 해외 파견 기회도 있습니다.',
        'tip': '7급 공채 합격자는 5급 승진까지 평균 15~20년이 소요되며, 승진 시 연봉이 크게 상승합니다.'
    },
    {
        'slug': 'pharmacist', 'name': '약사',
        'desc': '약국·병원 근무 약사의 연봉과 실수령액을 정리했습니다.',
        'keyword': '약사 연봉',
        'salaries': [('신입 (봉직)', 5000), ('경력 3년차', 5800), ('경력 7년차', 6500), ('관리약사', 7000), ('개국약사 (평균)', 9000)],
        'info': '약사는 6년제 약학대학 졸업 후 면허를 취득해야 합니다. 봉직약사는 약국 또는 병원에 고용되어 근무하며, 개국약사는 본인이 약국을 운영합니다. 병원약사는 봉직약사보다 초봉이 낮을 수 있으나, 경력에 따른 상승폭이 큽니다.',
        'tip': '약사 인력난으로 지방 약국의 경우 연봉 7,000만원 이상을 제시하는 곳도 많습니다.'
    },
    {
        'slug': 'developer', 'name': 'IT 개발자',
        'desc': 'SW 개발자의 경력별 연봉과 실수령액을 정리했습니다.',
        'keyword': '개발자 연봉',
        'salaries': [('신입 (중소기업)', 3500), ('신입 (대기업/스타트업)', 5000), ('경력 3년차', 5500), ('경력 5년차', 7000), ('시니어 (10년차+)', 10000)],
        'info': 'IT 개발자는 기업 규모와 기술 스택에 따라 연봉 편차가 매우 큽니다. 네카라쿠배(네이버·카카오·라인·쿠팡·배달의민족) 등 대형 IT 기업은 신입도 5,000만원 이상을 제시합니다. 프론트엔드, 백엔드, AI/ML 등 분야별로도 차이가 있습니다.',
        'tip': 'IT 업계는 스톡옵션, RSU(양도제한조건부주식) 등 주식 보상이 연봉 외 큰 비중을 차지합니다. 이는 실수령액에 포함되지 않지만, 총 보상 패키지에서 중요한 부분입니다.'
    },
    {
        'slug': 'designer', 'name': '디자이너',
        'desc': 'UI/UX, 그래픽, 제품 디자이너의 연봉과 실수령액을 정리했습니다.',
        'keyword': '디자이너 연봉',
        'salaries': [('신입 (중소기업)', 2800), ('신입 (대기업)', 4000), ('경력 3년차', 4500), ('경력 5년차', 5500), ('시니어/리드', 7500)],
        'info': '디자이너는 분야(UI/UX, 그래픽, 제품, 영상)와 기업 규모에 따라 연봉 차이가 큽니다. IT 기업의 UX 디자이너는 개발자와 비슷한 수준의 연봉을 받으며, 포트폴리오 퀄리티가 연봉 협상에 중요한 역할을 합니다.',
        'tip': '프리랜서 디자이너는 3.3% 원천징수 후 종합소득세 신고를 해야 합니다. 4대보험이 적용되지 않아 실수령액 계산이 다릅니다.'
    },
    {
        'slug': 'accountant', 'name': '회계사',
        'desc': '공인회계사(CPA)의 경력별 연봉과 실수령액을 정리했습니다.',
        'keyword': '회계사 연봉',
        'salaries': [('수습 (1년차)', 4500), ('주니어 (3년차)', 5500), ('시니어 (5년차)', 7000), ('매니저 (8년차)', 9000), ('파트너', 15000)],
        'info': '공인회계사는 4대 회계법인(삼일, 삼정, 한영, 안진)과 중소 회계법인, 일반 기업으로 진출 경로가 나뉩니다. 4대 법인 수습 연봉은 약 4,500만원이며, 바쁜 시즌(1~3월)에는 초과근무수당이 상당합니다.',
        'tip': '회계사는 퇴직 후 개업하거나 기업 CFO로 이직하는 경우가 많으며, 이 경우 연봉이 크게 상승합니다.'
    },
    {
        'slug': 'lawyer', 'name': '변호사',
        'desc': '변호사의 경력별 연봉과 실수령액을 정리했습니다.',
        'keyword': '변호사 연봉',
        'salaries': [('로펌 신입 (대형)', 10000), ('로펌 신입 (중소)', 5000), ('경력 5년차', 9000), ('경력 10년차', 13000), ('파트너', 20000)],
        'info': '변호사는 대형 로펌(김앤장, 율촌, 광장 등)과 중소 로펌, 개인 사무소 간 연봉 차이가 매우 큽니다. 대형 로펌 신입은 연봉 1억 이상이 일반적이나, 야근과 주말 근무가 잦습니다. 중소 로펌이나 공익 변호사는 이보다 낮을 수 있습니다.',
        'tip': '변호사 개업 시에는 사업소득으로 분류되어 종합소득세 신고가 필요하며, 4대보험 대신 지역가입 건강보험료를 납부합니다.'
    },
    {
        'slug': 'bank-clerk', 'name': '은행원',
        'desc': '시중은행 행원의 연봉과 실수령액을 정리했습니다.',
        'keyword': '은행원 연봉',
        'salaries': [('신입행원', 4500), ('대리 (4년차)', 5500), ('과장 (8년차)', 7000), ('차장 (12년차)', 8500), ('부장 (18년차)', 10000)],
        'info': '시중은행(KB국민, 신한, 하나, 우리, NH농협)은 금융권 중 가장 안정적인 연봉 체계를 가지고 있습니다. 성과급이 기본급의 최대 800%까지 나올 수 있어, 실제 연간 수입은 기본 연봉보다 훨씬 높습니다.',
        'tip': '은행 성과급은 근로소득세가 적용되므로 고율 과세 구간에 해당할 수 있습니다. 성과급 수령 시 연말정산을 꼼꼼히 확인하세요.'
    },
    {
        'slug': 'delivery-rider', 'name': '배달 라이더',
        'desc': '배달 플랫폼 라이더의 월수입과 세금을 정리했습니다.',
        'keyword': '배달 라이더 수입',
        'salaries': [('파트타임 (주3일)', 1500), ('일반 (주5일)', 3000), ('전업 (주6일)', 4200), ('하이퍼 (주6일, 12시간)', 5500)],
        'info': '배달 라이더는 프리랜서(개인사업자)로 분류되어 3.3% 원천징수 후 매년 5월 종합소득세를 신고합니다. 4대보험 가입 의무가 없어 국민연금, 건강보험을 지역가입으로 별도 납부해야 합니다. 오토바이 유지비, 보험료, 기름값 등 필요경비를 공제할 수 있습니다.',
        'tip': '라이더는 산재보험 특례 적용 대상입니다. 플랫폼에서 산재보험료를 부담하므로 업무 중 사고 시 보장받을 수 있습니다.'
    },
    {
        'slug': 'soldier', 'name': '직업군인',
        'desc': '직업군인(부사관·장교)의 계급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '직업군인 연봉',
        'salaries': [('하사 (신임)', 2800), ('중사 (7년차)', 3500), ('상사 (15년차)', 4500), ('소위 (신임장교)', 3200), ('대위 (8년차)', 4800)],
        'info': '직업군인은 군인봉급표에 따라 급여를 받으며, 군인연금에 가입됩니다. 기본급 외에 직책수당, 비상근무수당, 전투근무수당, 위험근무수당 등이 추가됩니다. 관사(숙소) 제공, 식비 지원 등 복리후생이 있어 실질적인 생활비 부담이 적습니다.',
        'tip': '군인은 국민연금 대신 군인연금(기여금 7%)을 납부하며, 20년 이상 복무 시 퇴직 후 연금을 수령합니다.'
    },
]

# ── 대기업 데이터 ──
COMPANIES = [
    {
        'slug': 'samsung', 'name': '삼성전자',
        'desc': '삼성전자 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '삼성전자 연봉',
        'salaries': [('CL1 (신입)', 5200), ('CL2 (대리급)', 6500), ('CL3 (과장급)', 8000), ('CL4 (부장급)', 10000), ('임원', 15000)],
        'info': '삼성전자는 국내 최대 시가총액 기업으로, 기본급 외에 성과급(OPI/TAI)이 최대 연봉의 50% 수준으로 지급됩니다. 2024년부터 직급체계를 CL(Career Level) 1~4로 단순화했으며, 직급별 체류 기간에 따라 승진이 결정됩니다.',
        'tip': '삼성전자 성과급은 사업부 실적에 따라 0~50%까지 차이가 크며, DS(반도체) 부문과 DX(가전·모바일) 부문의 성과급 수준이 다릅니다.'
    },
    {
        'slug': 'hyundai-motor', 'name': '현대자동차',
        'desc': '현대자동차 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '현대자동차 연봉',
        'salaries': [('사원 (신입)', 5000), ('대리 (4년차)', 6200), ('과장 (8년차)', 7500), ('차장 (13년차)', 9000), ('부장', 11000)],
        'info': '현대자동차는 완성차 업계 1위로, 기본급에 성과급(PS), 격려금 등이 추가됩니다. 생산직은 통상임금 기반 교대수당, 연장근로수당이 높아 사무직보다 실수령액이 높을 수 있습니다. 울산·아산 등 공장 근무 시 기숙사/관사 제공 혜택이 있습니다.',
        'tip': '현대차 생산직 평균 연봉은 약 9,000만원(수당 포함)으로, 사무직 과장급과 비슷한 수준입니다.'
    },
    {
        'slug': 'sk-hynix', 'name': 'SK하이닉스',
        'desc': 'SK하이닉스 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': 'SK하이닉스 연봉',
        'salaries': [('사원 (신입)', 5000), ('선임 (4년차)', 6300), ('책임 (8년차)', 8000), ('수석 (13년차)', 10000), ('임원', 15000)],
        'info': 'SK하이닉스는 반도체 메모리 2위 기업으로, 삼성전자 반도체 부문과 경쟁 관계입니다. 성과급은 업황에 따라 크게 변동하며, 호황기에는 연봉의 50% 이상이 성과급으로 지급되기도 합니다. 이천·청주 캠퍼스 근무 시 셔틀버스, 기숙사 등 복리후생이 제공됩니다.',
        'tip': 'SK하이닉스는 AI 반도체(HBM) 수요 증가로 최근 성과급이 크게 상승했습니다.'
    },
    {
        'slug': 'naver', 'name': '네이버',
        'desc': '네이버 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '네이버 연봉',
        'salaries': [('신입', 5500), ('경력 3년차', 7000), ('경력 5년차', 8500), ('경력 10년차', 11000), ('리드/매니저', 14000)],
        'info': '네이버는 IT 업계 최고 수준의 연봉을 제공합니다. 기본급 외에 스톡옵션(또는 RSU), 성과급, 복지포인트 등이 포함됩니다. 2024년부터 직급 없는 수평적 조직문화를 강화했으며, 판교 본사 근무 기준 유연근무제, 재택근무가 가능합니다.',
        'tip': '네이버 RSU(양도제한조건부주식)는 4년에 걸쳐 지급되며, 주가 상승 시 상당한 추가 수익이 발생합니다. RSU 수령 시 근로소득세가 과세됩니다.'
    },
    {
        'slug': 'kakao', 'name': '카카오',
        'desc': '카카오 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '카카오 연봉',
        'salaries': [('신입', 5000), ('경력 3년차', 6500), ('경력 5년차', 8000), ('경력 10년차', 10000), ('리드/매니저', 13000)],
        'info': '카카오는 카카오톡을 기반으로 한 IT 대기업입니다. 기본급, 성과급 외에 스톡옵션이 주요 보상으로 포함됩니다. 판교 본사 근무이며, 자유로운 근무 환경과 4.5일 근무제(매주 금요일 오후 쉼) 등이 특징입니다.',
        'tip': '카카오 계열사(카카오뱅크, 카카오페이 등)는 본사와 연봉 체계가 다를 수 있으며, 금융 계열사는 일반적으로 더 높은 연봉을 제공합니다.'
    },
    {
        'slug': 'coupang', 'name': '쿠팡',
        'desc': '쿠팡 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '쿠팡 연봉',
        'salaries': [('신입 (사무직)', 4500), ('경력 3년차', 6000), ('경력 5년차', 7500), ('시니어', 10000), ('디렉터', 15000)],
        'info': '쿠팡은 이커머스 1위 기업으로, 미국 NYSE에 상장되어 있습니다. 사무직은 기본급+RSU 체계이며, 물류센터 근무자(쿠팡맨)는 시급제+각종 수당 체계입니다. 성과에 따른 보상이 크며, 빠른 승진이 가능합니다.',
        'tip': '쿠팡 RSU는 미국 주식으로 지급되므로, 환차익/환차손이 발생할 수 있으며, 해외주식 양도소득세 신고가 필요합니다.'
    },
    {
        'slug': 'lg-energy', 'name': 'LG에너지솔루션',
        'desc': 'LG에너지솔루션 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': 'LG에너지솔루션 연봉',
        'salaries': [('사원 (신입)', 5000), ('선임 (4년차)', 6200), ('책임 (8년차)', 7800), ('수석 (13년차)', 9500), ('임원', 14000)],
        'info': 'LG에너지솔루션은 글로벌 배터리 1위 기업으로, 전기차 시장 성장과 함께 급성장하고 있습니다. 오창·대전 공장 근무자가 많으며, 해외(미국·폴란드·인도네시아) 파견 기회도 있습니다. 파견 시 해외근무수당이 추가됩니다.',
        'tip': 'LG에너지솔루션은 최근 배터리 업황 변동에 따라 성과급 수준이 달라지고 있습니다.'
    },
    {
        'slug': 'posco', 'name': '포스코',
        'desc': '포스코(포스코홀딩스/포스코퓨처엠) 직급별 연봉과 실수령액을 정리했습니다.',
        'keyword': '포스코 연봉',
        'salaries': [('사원 (신입)', 4800), ('대리 (4년차)', 6000), ('과장 (8년차)', 7500), ('차장 (13년차)', 9000), ('부장', 11000)],
        'info': '포스코는 철강 업계 1위이며, 포항·광양 제철소가 주요 근무지입니다. 교대근무자는 교대수당이 추가되어 사무직보다 실수령액이 높을 수 있습니다. 포스코홀딩스, 포스코퓨처엠 등 계열사별로 연봉 체계가 다릅니다.',
        'tip': '포스코는 관사(사택) 제공, 자녀 학자금 지원 등 복리후생이 좋아 실질적인 생활비 절감 효과가 큽니다.'
    },
]

# ── 네비게이션 HTML (최신 버전) ──
NAV_HTML = '''<!-- 네비게이션 -->
<nav class="nav">
    <div class="nav-inner">
        <a href="index.html" class="nav-logo">월급<span>연구소</span></a>
        <div class="nav-menu">
            <div class="nav-item">
                <button class="nav-item-btn">월급 받을 때 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="index.html"><div class="nav-dropdown-dot" style="background:#2563EB;"></div>연봉 실수령액</a>
                    <a href="minimum-wage.html"><div class="nav-dropdown-dot" style="background:#F59E0B;"></div>최저시급 계산기</a>
                    <a href="holiday-pay.html"><div class="nav-dropdown-dot" style="background:#059669;"></div>주휴수당 계산기</a>
                    <a href="insurance.html"><div class="nav-dropdown-dot" style="background:#8B5CF6;"></div>4대보험 계산기</a>
                    <a href="salary-table.html"><div class="nav-dropdown-dot" style="background:#EF4444;"></div>실수령액 표</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">세금 낼 때 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="income-tax.html"><div class="nav-dropdown-dot" style="background:#F59E0B;"></div>종합소득세</a>
                    <a href="gift-tax.html"><div class="nav-dropdown-dot" style="background:#059669;"></div>증여세 계산기</a>
                    <a href="acquisition-tax.html"><div class="nav-dropdown-dot" style="background:#EF4444;"></div>취득세 계산기</a>
                    <a href="tax-guide.html"><div class="nav-dropdown-dot" style="background:#2563EB;"></div>연말정산 가이드</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">병원 갈 때 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="medical-tax.html"><div class="nav-dropdown-dot" style="background:#EC4899;"></div>의료비 세액공제</a>
                    <a href="silbi.html"><div class="nav-dropdown-dot" style="background:#06B6D4;"></div>실비보험 계산기</a>
                    <a href="guide-medical-tax.html"><div class="nav-dropdown-dot" style="background:#F472B6;"></div>의료비 공제 가이드</a>
                    <a href="guide-silbi.html"><div class="nav-dropdown-dot" style="background:#22D3EE;"></div>실비보험 가이드</a>
                </div>
            </div>
            <div class="nav-item">
                <button class="nav-item-btn">퇴사할 때 <svg viewBox="0 0 12 12"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
                <div class="nav-dropdown">
                    <a href="retirement.html"><div class="nav-dropdown-dot" style="background:#059669;"></div>퇴직금 계산기</a>
                    <a href="unemployment.html"><div class="nav-dropdown-dot" style="background:#8B5CF6;"></div>실업급여 계산기</a>
                </div>
            </div>
        </div>
        <div class="lang-selector">
                <button class="lang-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> KO</button>
                <div class="lang-dropdown">
                    <a href="index.html" class="active">한국어</a>
                    <a href="en.html">English</a>
                    <a href="zh.html">中文</a>
                    <a href="ja.html">日本語</a>
                </div>
            </div>
        <button class="nav-mobile-btn" onclick="document.querySelector('.nav-mobile').classList.toggle('open')">☰</button>
    </div>
    <div class="nav-mobile">
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">월급 받을 때</div>
            <a href="index.html">연봉 실수령액</a>
            <a href="minimum-wage.html">최저시급 계산기</a>
            <a href="holiday-pay.html">주휴수당 계산기</a>
            <a href="insurance.html">4대보험 계산기</a>
            <a href="salary-table.html">실수령액 표</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">세금 낼 때</div>
            <a href="income-tax.html">종합소득세 계산기</a>
            <a href="gift-tax.html">증여세 계산기</a>
            <a href="acquisition-tax.html">취득세 계산기</a>
            <a href="tax-guide.html">연말정산 가이드</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">병원 갈 때</div>
            <a href="medical-tax.html">의료비 세액공제</a>
            <a href="silbi.html">실비보험 계산기</a>
            <a href="guide-medical-tax.html">의료비 공제 가이드</a>
            <a href="guide-silbi.html">실비보험 가이드</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">퇴사할 때</div>
            <a href="retirement.html">퇴직금 계산기</a>
            <a href="unemployment.html">실업급여 계산기</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">기타</div>
            <a href="about.html">소개</a>
            <a href="contact.html">문의</a>
            <a href="privacy.html">개인정보처리방침</a>
        </div>
        <div class="nav-mobile-group">
            <div class="nav-mobile-title">Language</div>
            <a href="index.html" style="color:var(--accent);font-weight:700;">한국어</a>
            <a href="en.html">English</a>
            <a href="zh.html">中文</a>
            <a href="ja.html">日本語</a>
        </div>
    </div>
</nav>'''

def gen_deduction_items(s):
    """공제 항목 HTML 생성"""
    max_val = s['np']
    items = [
        ('국민연금', s['np'], '#2563EB'),
        ('건강보험', s['hi'], '#8B5CF6'),
        ('장기요양보험', s['ltc'], '#A78BFA'),
        ('고용보험', s['ei'], '#F59E0B'),
        ('소득세', s['tax'], '#EF4444'),
        ('지방소득세', s['local_tax'], '#9CA3AF'),
    ]
    html = ''
    for name, amount, color in items:
        pct = amount / max_val * 100 if max_val > 0 else 0
        html += f'''
                    <div class="b-item">
                        <div class="b-dot" style="background:{color};"></div>
                        <div class="b-info">
                            <div class="b-name">{name}</div>
                            <div class="b-bar-wrap">
                                <div class="b-bar" style="background:{color}; width:{pct:.1f}%;"></div>
                            </div>
                        </div>
                        <div class="b-amount">-{fmt(amount)}원</div>
                    </div>'''
    return html

def gen_salary_rows(salaries, is_job=True):
    """경력별 실수령액 테이블 행 HTML"""
    rows = ''
    for label, annual_man in salaries:
        s = calc_salary(annual_man * 10000)
        rows += f'''                        <tr>
                            <td>{label}</td>
                            <td>{fmt_man(annual_man)}</td>
                            <td>{fmt(s['monthly'])}원</td>
                            <td>{fmt(s['total_ded'])}원</td>
                            <td class="accent">{fmt(s['net'])}원</td>
                        </tr>
'''
    return rows

def generate_page(data, page_type='job'):
    """직종/기업 페이지 HTML 생성"""
    slug = data['slug']
    name = data['name']
    desc = data['desc']
    keyword = data['keyword']
    salaries = data['salaries']
    info = data['info']
    tip = data['tip']

    # 대표 연봉으로 상세 계산 (두 번째 항목 기준)
    rep_idx = 1 if len(salaries) > 1 else 0
    rep_label, rep_annual = salaries[rep_idx]
    rep = calc_salary(rep_annual * 10000)

    prefix = 'job' if page_type == 'job' else 'company'
    filename = f"{prefix}-{slug}.html"
    url = f"https://salarykorea.site/{prefix}-{slug}"

    if page_type == 'job':
        title = f"2026년 {name} 연봉 실수령액 — 경력별 월급 총정리 | 월급연구소"
        h1 = f"{name} 연봉 실수령액"
        breadcrumb = "홈 &gt; 직종별 연봉"
        sub = f"2026년 기준 · {name} 경력별 연봉과 실수령액"
        schema_cat = f"{name} 급여"
    else:
        title = f"2026년 {name} 연봉 실수령액 — 직급별 월급 총정리 | 월급연구소"
        h1 = f"{name} 연봉 실수령액"
        breadcrumb = "홈 &gt; 기업별 연봉"
        sub = f"2026년 기준 · {name} 직급별 연봉과 실수령액"
        schema_cat = f"{name} 급여"

    meta_desc = f"2026년 기준 {name}의 연봉과 실수령액을 {'경력별' if page_type=='job' else '직급별'}로 정리했습니다. {rep_label} 연봉 {fmt_man(rep_annual)}의 월 실수령액은 {fmt(rep['net'])}원입니다."

    # 관련 페이지 링크
    if page_type == 'job':
        related_items = [j for j in JOBS if j['slug'] != slug][:5]
        related_prefix = 'job'
    else:
        related_items = [c for c in COMPANIES if c['slug'] != slug][:5]
        related_prefix = 'company'

    related_links = ''
    for r in related_items:
        related_links += f'                <a href="{related_prefix}-{r["slug"]}.html" style="padding:8px 16px; background:var(--surface-alt); border:1px solid var(--border); border-radius:8px; font-size:0.82rem; font-weight:600; color:var(--text-primary); text-decoration:none; transition:all 0.15s;">{r["name"]}</a>\n'

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="ro2hwYnXOh_1OXnZ5hyFkJ663ACoqYU8gvHgL0g2rcI" />
    <meta name="naver-site-verification" content="c52838d57daadbdbae1bceb6c6131ab62ee07e2a" />
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{keyword}, {name} 실수령액, {name} 월급, 2026 {name} 연봉">
    <meta property="og:title" content="{name} 연봉 실수령액 — {'경력별' if page_type=='job' else '직급별'} 총정리">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="website">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="common.css">
    <style>
        .result-hero {{ background: linear-gradient(135deg, var(--accent-dark), #3B82F6); border-radius: 16px; padding: 32px 28px; text-align: center; margin-bottom: 24px; }}
        .result-hero-label {{ font-size: 0.75rem; color: rgba(255,255,255,0.5); font-weight: 500; letter-spacing: 0.5px; margin-bottom: 8px; }}
        .result-hero-amount {{ font-size: 2.8rem; font-weight: 900; color: white; font-family: 'Inter', sans-serif; letter-spacing: -2px; }}
        .result-hero-unit {{ font-size: 0.8rem; color: rgba(255,255,255,0.4); margin-top: 4px; }}
        .result-hero-stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: rgba(255,255,255,0.08); border-radius: 12px; overflow: hidden; margin-top: 20px; }}
        .rh-stat {{ background: linear-gradient(135deg, var(--accent-dark), #3B82F6); padding: 16px 12px; text-align: center; }}
        .rh-stat-label {{ font-size: 0.68rem; color: rgba(255,255,255,0.4); margin-bottom: 4px; }}
        .rh-stat-val {{ font-size: 0.88rem; color: rgba(255,255,255,0.95); font-weight: 700; font-family: 'Inter', sans-serif; }}
        @media (max-width: 768px) {{
            .result-hero-amount {{ font-size: 2.2rem; }}
            .rh-stat-val {{ font-size: 0.78rem; }}
        }}
        .b-item {{ display: flex; align-items: center; padding: 14px 0; border-bottom: 1px solid #F3F4F6; }}
        .b-item:last-child {{ border-bottom: none; }}
        .b-dot {{ width: 6px; height: 6px; border-radius: 50%; margin-right: 12px; flex-shrink: 0; }}
        .b-info {{ flex: 1; }}
        .b-name {{ font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px; }}
        .b-bar-wrap {{ background: #F3F4F6; border-radius: 3px; height: 4px; overflow: hidden; }}
        .b-bar {{ height: 100%; border-radius: 3px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); }}
        .b-amount {{ font-size: 0.88rem; font-weight: 700; color: var(--text-primary); font-family: 'Inter', sans-serif; margin-left: 12px; min-width: 90px; text-align: right; }}
        .b-total {{ display: flex; justify-content: space-between; padding: 16px 0 0; margin-top: 4px; border-top: 1px solid var(--text-primary); }}
        .b-total-label {{ font-size: 0.88rem; font-weight: 700; }}
        .b-total-val {{ font-size: 0.95rem; font-weight: 800; color: var(--accent); font-family: 'Inter', sans-serif; }}
        .data-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .data-table th {{ background: var(--surface-alt); padding: 10px 12px; text-align: center; font-weight: 700; color: var(--text-secondary); font-size: 0.8rem; }}
        .data-table th:first-child {{ text-align: left; }}
        .data-table td {{ padding: 12px; border-bottom: 1px solid #F3F4F6; text-align: center; color: var(--text-primary); }}
        .data-table td:first-child {{ text-align: left; font-weight: 600; color: var(--text-secondary); }}
        .data-table .accent {{ color: var(--accent); font-weight: 700; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; align-items: start; }}
        .salary-links {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
        .salary-links a {{ display: inline-block; padding: 8px 16px; font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); background: var(--surface-alt); border-radius: 8px; text-decoration: none; transition: all 0.15s; }}
        .salary-links a:hover {{ color: var(--accent); background: var(--accent-light); }}
        .ad-wrap {{ text-align: center; margin-bottom: 24px; }}
    </style>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3416211588228348" crossorigin="anonymous"></script>
    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{name} 연봉 실수령액",
    "description": "{meta_desc}",
    "url": "{url}",
    "isPartOf": {{
        "@type": "WebSite",
        "name": "월급연구소",
        "url": "https://salarykorea.site"
    }},
    "about": {{
        "@type": "FinancialProduct",
        "name": "{schema_cat}",
        "category": "Salary"
    }}
}}
    </script>
</head>
<body>

{NAV_HTML}

<div class="page">

    <div class="page-header">
        <div class="breadcrumb">{breadcrumb}</div>
        <h1>{h1}</h1>
        <p>{sub}</p>
    </div>

    <!-- 메인 결과 -->
    <div class="result-hero">
        <div class="result-hero-label">{rep_label} 월 실수령액</div>
        <div class="result-hero-amount">{fmt(rep['net'])}<span style="font-size:0.5em; font-weight:700;">원</span></div>
        <div class="result-hero-unit">연봉 {fmt_man(rep_annual)} · 세전 월급 {fmt(rep['monthly'])}원</div>
        <div class="result-hero-stats">
            <div class="rh-stat">
                <div class="rh-stat-label">연 실수령액</div>
                <div class="rh-stat-val">{fmt(rep['annual_net'])}원</div>
            </div>
            <div class="rh-stat">
                <div class="rh-stat-label">공제율</div>
                <div class="rh-stat-val">{rep['ded_rate']}%</div>
            </div>
            <div class="rh-stat">
                <div class="rh-stat-label">월 공제합계</div>
                <div class="rh-stat-val">{fmt(rep['total_ded'])}원</div>
            </div>
        </div>
    </div>

    <!-- 2컬럼: 공제 상세 + 정보 -->
    <div class="two-col">
        <div class="card" style="margin-bottom:0;">
            <div class="card-header">
                <div class="card-title">공제 항목 상��</div>
                <div class="card-badge">{rep_label} 기준</div>
            </div>
            {gen_deduction_items(rep)}
            <div class="b-total">
                <div class="b-total-label">공제합계</div>
                <div class="b-total-val">-{fmt(rep['total_ded'])}원</div>
            </div>
        </div>

        <div class="info-card">
    <h2>{name} 연봉 상세 분석</h2>
    <p>{info}</p>
    <h3 style="font-size:0.92rem; font-weight:700; color:var(--text-primary); margin:16px 0 8px;">알아두면 좋은 팁</h3>
    <p>{tip}</p>
    <p>정확한 금액은 <a href="index.html" style="color:var(--accent); font-weight:700; text-decoration:none;">연봉 실수령액 계산기</a>에서 직접 계산해보세요.</p>
</div>
    </div>

    <!-- 경력/직급별 비교 -->
    <div class="card">
        <div class="card-header">
            <div class="card-title">{'경력별' if page_type=='job' else '직급별'} 연봉 실수령액 비교</div>
            <div class="card-badge">2026년</div>
        </div>
        <div style="overflow-x:auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>{'경력' if page_type=='job' else '직급'}</th>
                        <th>연봉</th>
                        <th>세전 월급</th>
                        <th>월 공제액</th>
                        <th>월 실수령액</th>
                    </tr>
                </thead>
                <tbody>
{gen_salary_rows(salaries, page_type=='job')}                </tbody>
            </table>
        </div>
    </div>

    <!-- 관련 {'직종' if page_type=='job' else '기업'} -->
    <div class="card">
        <div class="card-header">
            <div class="card-title">다른 {'직종' if page_type=='job' else '기업'} 연봉 보기</div>
        </div>
        <div class="salary-links">
{related_links}        </div>
    </div>

    <!-- 연봉별 상세 -->
    <div class="card">
        <div class="card-header">
            <div class="card-title">연봉별 실수령액 상세</div>
        </div>
        <div class="salary-links">
            <a href="salary-2400.html">연봉 2,400만원</a>
            <a href="salary-3000.html">연봉 3,000만원</a>
            <a href="salary-4000.html">연봉 4,000만원</a>
            <a href="salary-5000.html">연봉 5,000만원</a>
            <a href="salary-7000.html">연봉 7,000만원</a>
            <a href="salary-10000.html">연봉 1억원</a>
        </div>
    </div>

<footer class="footer">
    <div class="footer-links">
        <a href="about.html">소개</a>
        <a href="contact.html">문의하기</a>
        <a href="privacy.html">개인정보처리방침</a>
    </div>
    <div class="footer-copy">© 2026 월급연구소</div>
</footer>

</body>
</html>'''
    return filename, html


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generated = []

    print("=" * 50)
    print("  월급연구소 - 롱테일 SEO 페이지 생성기")
    print("=" * 50)

    # 직종별 페이지 생성
    print(f"\n📋 직종별 페이지 생성 중... ({len(JOBS)}개)")
    for job in JOBS:
        filename, html = generate_page(job, 'job')
        filepath = os.path.join(script_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated.append(filename)
        print(f"  ✅ {filename} — {job['name']}")

    # 기업별 페이지 생성
    print(f"\n🏢 기업별 페이지 생성 중... ({len(COMPANIES)}개)")
    for company in COMPANIES:
        filename, html = generate_page(company, 'company')
        filepath = os.path.join(script_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated.append(filename)
        print(f"  ✅ {filename} — {company['name']}")

    # sitemap 업데이트용 URL 출력
    print(f"\n📊 총 {len(generated)}개 페이지 생성 완료!")
    print(f"\n📝 sitemap.xml에 추가할 URL 목록:")
    for fn in generated:
        slug = fn.replace('.html', '')
        print(f"  https://salarykorea.site/{slug}")

    # sitemap 자동 업데이트
    sitemap_path = os.path.join(script_dir, 'sitemap.xml')
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap = f.read()

        new_entries = ''
        for fn in generated:
            slug = fn.replace('.html', '')
            url = f"https://salarykorea.site/{slug}"
            if url not in sitemap:
                new_entries += f'''    <url>
        <loc>{url}</loc>
        <lastmod>2026-04-03</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''

        if new_entries:
            sitemap = sitemap.replace('</urlset>', new_entries + '</urlset>')
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(sitemap)
            print(f"\n✅ sitemap.xml 자동 업데이트 완료!")

    print(f"\n🎯 다음 단계: ./push.sh 로 배포 후 색인 요청")


if __name__ == '__main__':
    main()
