/* ══════════════════════════════════════
   월급연구소 - 사이트 내 검색 (다국어 지원)
   ══════════════════════════════════════ */

(function() {
    'use strict';

    /* ── 현재 언어 감지 ── */
    var lang = (document.documentElement.lang || 'ko').toLowerCase().replace('-hans', '');
    // 'ko', 'en', 'zh', 'ja' 중 하나

    /* ── 언어별 UI 텍스트 ── */
    var UI = {
        ko: {
            placeholder: '페이지 검색 (예: 퇴직금, 삼성, 간호사...)',
            hint: '계산기, 가이드, 연봉, 직종, 기업명 등<br>원하는 키워드를 입력하세요',
            hintShortcut: ' 로 언제든 검색',
            noResult: '검색 결과가 없습니다',
            more: '건 더 있습니다'
        },
        en: {
            placeholder: 'Search pages (e.g. retirement, salary, insurance...)',
            hint: 'Search for calculators by keyword<br>e.g. salary, tax, insurance, minimum wage',
            hintShortcut: ' to search anytime',
            noResult: 'No results found',
            more: ' more results'
        },
        zh: {
            placeholder: '搜索页面（例：退休金、工资、保险...）',
            hint: '输入关键词搜索计算器<br>例：工资、税金、保险、最低工资',
            hintShortcut: ' 随时搜索',
            noResult: '未找到结果',
            more: ' 个更多结果'
        },
        ja: {
            placeholder: 'ページ検索（例：退職金、給料、保険...）',
            hint: 'キーワードで計算機を検索<br>例：給料、税金、保険、最低賃金',
            hintShortcut: ' でいつでも検索',
            noResult: '検索結果がありません',
            more: ' 件の追加結果'
        }
    };

    var ui = UI[lang] || UI.ko;

    /* ── 페이지 인덱스 (한국어) ── */
    var PAGES_KO = [
        // 계산기
        { t: '연봉 실수령액 계산기', u: 'index.html', c: '계산기', color: '#2563EB', k: '연봉 실수령액 월급 세후 세금 4대보험 공제 급여 연봉계산기 월급계산기' },
        { t: '최저시급 계산기', u: 'minimum-wage.html', c: '계산기', color: '#F59E0B', k: '최저시급 최저임금 알바 시급 주급 월급 아르바이트 2026' },
        { t: '연봉별 실수령액 표', u: 'salary-table.html', c: '계산기', color: '#EF4444', k: '연봉 실수령액 표 테이블 비교 세후 연봉표' },
        { t: '주휴수당 계산기', u: 'holiday-pay.html', c: '계산기', color: '#059669', k: '주휴수당 주휴 알바 수당 휴일' },
        { t: '4대보험 계산기', u: 'insurance.html', c: '계산기', color: '#8B5CF6', k: '4대보험 국민연금 건강보험 고용보험 산재보험 사대보험' },
        { t: '종합소득세 계산기', u: 'income-tax.html', c: '계산기', color: '#F59E0B', k: '종합소득세 소득세 세금 종소세 프리랜서' },
        { t: '증여세 계산기', u: 'gift-tax.html', c: '계산기', color: '#059669', k: '증여세 증여 세금 부모 자녀 가족 선물' },
        { t: '취득세 계산기', u: 'acquisition-tax.html', c: '계산기', color: '#EF4444', k: '취득세 부동산 집 아파트 매매 주택' },
        { t: '퇴직금 계산기', u: 'retirement.html', c: '계산기', color: '#059669', k: '퇴직금 퇴직 퇴사 근속 근무기간' },
        { t: '실업급여 계산기', u: 'unemployment.html', c: '계산기', color: '#8B5CF6', k: '실업급여 실업 퇴사 구직 고용센터 수급' },
        { t: '의료비 세액공제 계산기', u: 'medical-tax.html', c: '계산기', color: '#EC4899', k: '의료비 세액공제 병원 의료 세금 연말정산' },
        { t: '실비보험 계산기', u: 'silbi.html', c: '계산기', color: '#06B6D4', k: '실비보험 실손보험 보험 환급 병원비 실비' },

        // 가이드
        { t: '연봉 실수령액 가이드', u: 'guide-salary.html', c: '가이드', color: '#2563EB', k: '연봉 실수령액 가이드 월급 공제 설명' },
        { t: '최저시급 가이드', u: 'guide-minimum-wage.html', c: '가이드', color: '#F59E0B', k: '최저시급 최저임금 가이드 알바 설명' },
        { t: '주휴수당 가이드', u: 'guide-holiday-pay.html', c: '가이드', color: '#059669', k: '주휴수당 가이드 주휴 알바 설명' },
        { t: '4대보험 가이드', u: 'guide-insurance.html', c: '가이드', color: '#8B5CF6', k: '4대보험 가이드 국민연금 건강보험 설명 사대보험' },
        { t: '연말정산 가이드', u: 'guide-tax.html', c: '가이드', color: '#F59E0B', k: '연말정산 가이드 세금 소득공제 세액공제 13월의월급' },
        { t: '연말정산 총정리', u: 'tax-guide.html', c: '가이드', color: '#2563EB', k: '연말정산 세금 소득공제 세액공제 절세 환급' },
        { t: '실업급여 가이드', u: 'guide-unemployment.html', c: '가이드', color: '#8B5CF6', k: '실업급여 가이드 퇴사 구직 수급 설명' },
        { t: '퇴직금 가이드', u: 'guide-retirement.html', c: '가이드', color: '#059669', k: '퇴직금 가이드 퇴직 퇴사 설명' },
        { t: '프리랜서 세금 가이드', u: 'guide-freelancer.html', c: '가이드', color: '#EF4444', k: '프리랜서 가이드 3.3 사업소득 세금 종소세 원천징수' },
        { t: '의료비 공제 가이드', u: 'guide-medical-tax.html', c: '가이드', color: '#EC4899', k: '의료비 세액공제 가이드 병원 연말정산 설명' },
        { t: '실비보험 가이드', u: 'guide-silbi.html', c: '가이드', color: '#06B6D4', k: '실비보험 실손보험 가이드 보험 환급 설명' },
        { t: '종합소득세 가이드', u: 'guide-income-tax.html', c: '가이드', color: '#F59E0B', k: '종합소득세 종소세 가이드 프리랜서 사업자 경비율 5월 신고 세금' },

        // 연봉별 상세
        { t: '연봉 2,400만원 실수령액', u: 'salary-2400.html', c: '연봉별', color: '#6366F1', k: '2400만원 2400 연봉' },
        { t: '연봉 2,600만원 실수령액', u: 'salary-2600.html', c: '연봉별', color: '#6366F1', k: '2600만원 2600 연봉' },
        { t: '연봉 2,800만원 실수령액', u: 'salary-2800.html', c: '연봉별', color: '#6366F1', k: '2800만원 2800 연봉' },
        { t: '연봉 3,000만원 실수령액', u: 'salary-3000.html', c: '연봉별', color: '#6366F1', k: '3000만원 3000 연봉 삼천' },
        { t: '연봉 3,500만원 실수령액', u: 'salary-3500.html', c: '연봉별', color: '#6366F1', k: '3500만원 3500 연봉' },
        { t: '연봉 4,000만원 실수령액', u: 'salary-4000.html', c: '연봉별', color: '#6366F1', k: '4000만원 4000 연봉 사천' },
        { t: '연봉 4,500만원 실수령액', u: 'salary-4500.html', c: '연봉별', color: '#6366F1', k: '4500만원 4500 연봉' },
        { t: '연봉 5,000만원 실수령액', u: 'salary-5000.html', c: '연봉별', color: '#6366F1', k: '5000만원 5000 연봉 오천' },
        { t: '연봉 5,500만원 실수령액', u: 'salary-5500.html', c: '연봉별', color: '#6366F1', k: '5500만원 5500 연봉' },
        { t: '연봉 6,000만원 실수령액', u: 'salary-6000.html', c: '연봉별', color: '#6366F1', k: '6000만원 6000 연봉 육천' },
        { t: '연봉 7,000만원 실수령액', u: 'salary-7000.html', c: '연봉별', color: '#6366F1', k: '7000만원 7000 연봉 칠천' },
        { t: '연봉 8,000만원 실수령액', u: 'salary-8000.html', c: '연봉별', color: '#6366F1', k: '8000만원 8000 연봉 팔천' },
        { t: '연봉 9,000만원 실수령액', u: 'salary-9000.html', c: '연봉별', color: '#6366F1', k: '9000만원 9000 연봉 구천' },
        { t: '연봉 1억원 실수령액', u: 'salary-10000.html', c: '연봉별', color: '#6366F1', k: '1억 10000만원 10000 연봉 억대' },
        { t: '연봉 1.5억원 실수령액', u: 'salary-15000.html', c: '연봉별', color: '#6366F1', k: '1.5억 15000만원 15000 연봉' },
        { t: '연봉 2억원 실수령액', u: 'salary-20000.html', c: '연봉별', color: '#6366F1', k: '2억 20000만원 20000 연봉' },

        // 직종별
        { t: '간호사 연봉 실수령액', u: 'job-nurse.html', c: '직종별', color: '#EC4899', k: '간호사 연봉 병원 의료 nurse' },
        { t: '교사 연봉 실수령액', u: 'job-teacher.html', c: '직종별', color: '#F59E0B', k: '교사 선생님 연봉 학교 교육 teacher' },
        { t: '경찰 연봉 실수령액', u: 'job-police.html', c: '직종별', color: '#2563EB', k: '경찰 경찰관 연봉 공무원 police' },
        { t: '소방관 연봉 실수령액', u: 'job-firefighter.html', c: '직종별', color: '#EF4444', k: '소방관 소방 연봉 공무원 firefighter' },
        { t: '9급 공무원 연봉 실수령액', u: 'job-civil-servant-9.html', c: '직종별', color: '#059669', k: '9급 공무원 연봉 행정 civil servant' },
        { t: '7급 공무원 연봉 실수령액', u: 'job-civil-servant-7.html', c: '직종별', color: '#059669', k: '7급 공무원 연봉 행정 civil servant' },
        { t: '약사 연봉 실수령액', u: 'job-pharmacist.html', c: '직종별', color: '#8B5CF6', k: '약사 연봉 약국 의료 pharmacist' },
        { t: '개발자 연봉 실수령액', u: 'job-developer.html', c: '직종별', color: '#06B6D4', k: '개발자 프로그래머 IT 연봉 developer 코딩' },
        { t: '디자이너 연봉 실수령액', u: 'job-designer.html', c: '직종별', color: '#EC4899', k: '디자이너 연봉 UI UX 그래픽 designer' },
        { t: '회계사 연봉 실수령액', u: 'job-accountant.html', c: '직종별', color: '#F59E0B', k: '회계사 공인회계사 CPA 연봉 accountant' },
        { t: '변호사 연봉 실수령액', u: 'job-lawyer.html', c: '직종별', color: '#18191B', k: '변호사 법조 법률 연봉 lawyer 로펌' },
        { t: '은행원 연봉 실수령액', u: 'job-bank-clerk.html', c: '직종별', color: '#2563EB', k: '은행원 은행 금융 연봉 bank' },
        { t: '배달 라이더 연봉 실수령액', u: 'job-delivery-rider.html', c: '직종별', color: '#059669', k: '배달 라이더 배달기사 연봉 쿠팡이츠 배민' },
        { t: '군인 연봉 실수령액', u: 'job-soldier.html', c: '직종별', color: '#6B7280', k: '군인 장교 부사관 연봉 국방 soldier 병사' },

        // 기업별
        { t: '삼성전자 연봉 실수령액', u: 'company-samsung.html', c: '기업별', color: '#1428A0', k: '삼성전자 삼성 samsung 연봉 대기업' },
        { t: '현대자동차 연봉 실수령액', u: 'company-hyundai-motor.html', c: '기업별', color: '#002C5F', k: '현대자동차 현대 hyundai 연봉 대기업 자동차' },
        { t: 'SK하이닉스 연봉 실수령액', u: 'company-sk-hynix.html', c: '기업별', color: '#ED1C24', k: 'SK하이닉스 SK 반도체 연봉 대기업' },
        { t: '네이버 연봉 실수령액', u: 'company-naver.html', c: '기업별', color: '#03C75A', k: '네이버 naver IT 연봉 대기업 포털' },
        { t: '카카오 연봉 실수령액', u: 'company-kakao.html', c: '기업별', color: '#FEE500', k: '카카오 kakao IT 연봉 대기업 카톡' },
        { t: '쿠팡 연봉 실수령액', u: 'company-coupang.html', c: '기업별', color: '#E31937', k: '쿠팡 coupang 이커머스 연봉 대기업 배달' },
        { t: 'LG에너지솔루션 연봉 실수령액', u: 'company-lg-energy.html', c: '기업별', color: '#A50034', k: 'LG에너지솔루션 LG 배터리 연봉 대기업' },
        { t: '포스코 연봉 실수령액', u: 'company-posco.html', c: '기업별', color: '#005386', k: '포스코 posco 철강 연봉 대기업' },

        // 기타
        { t: '소개', u: 'about.html', c: '기타', color: '#9CA3AF', k: '소개 월급연구소 정보 about' },
        { t: '문의하기', u: 'contact.html', c: '기타', color: '#9CA3AF', k: '문의 연락 contact 이메일' },
        { t: '개인정보처리방침', u: 'privacy.html', c: '기타', color: '#9CA3AF', k: '개인정보 처리방침 privacy 정책' },

        // 다국어 전환
        { t: 'English (영어)', u: 'en.html', c: '언어', color: '#2563EB', k: 'english 영어 영문' },
        { t: '中文 (중국어)', u: 'zh.html', c: '언어', color: '#EF4444', k: '중국어 중문 chinese' },
        { t: '日本語 (일본어)', u: 'ja.html', c: '언어', color: '#EC4899', k: '일본어 일문 japanese' }
    ];

    /* ── 페이지 인덱스 (English) ── */
    var PAGES_EN = [
        { t: 'Salary Calculator', u: 'en.html', c: 'Calculator', color: '#2563EB', k: 'salary take-home pay after tax net income calculator' },
        { t: 'Minimum Wage Calculator', u: 'minimum-wage-en.html', c: 'Calculator', color: '#F59E0B', k: 'minimum wage hourly pay part-time 2026' },
        { t: 'Salary Comparison Table', u: 'salary-table-en.html', c: 'Calculator', color: '#EF4444', k: 'salary table comparison chart net pay' },
        { t: 'Holiday Pay Calculator', u: 'holiday-pay-en.html', c: 'Calculator', color: '#059669', k: 'holiday pay weekly holiday allowance' },
        { t: 'Insurance Calculator', u: 'insurance-en.html', c: 'Calculator', color: '#8B5CF6', k: 'insurance pension health employment national 4 major' },
        { t: 'Income Tax Calculator', u: 'income-tax-en.html', c: 'Calculator', color: '#F59E0B', k: 'income tax comprehensive freelancer tax rate' },
        { t: 'Gift Tax Calculator', u: 'gift-tax-en.html', c: 'Calculator', color: '#059669', k: 'gift tax donation family inheritance' },
        { t: 'Acquisition Tax Calculator', u: 'acquisition-tax-en.html', c: 'Calculator', color: '#EF4444', k: 'acquisition tax property house apartment real estate' },
        { t: 'Retirement Pay Calculator', u: 'retirement-en.html', c: 'Calculator', color: '#059669', k: 'retirement severance pay resign tenure' },
        { t: 'Unemployment Benefits Calculator', u: 'unemployment-en.html', c: 'Calculator', color: '#8B5CF6', k: 'unemployment benefits jobseeker allowance' },
        { t: 'Medical Tax Deduction Calculator', u: 'medical-tax-en.html', c: 'Calculator', color: '#EC4899', k: 'medical tax deduction hospital healthcare' },
        { t: 'Health Insurance Calculator', u: 'silbi-en.html', c: 'Calculator', color: '#06B6D4', k: 'health insurance reimbursement hospital copay' },
        // 언어 전환
        { t: '한국어 (Korean)', u: 'index.html', c: 'Language', color: '#059669', k: 'korean 한국어' },
        { t: '中文 (Chinese)', u: 'zh.html', c: 'Language', color: '#EF4444', k: 'chinese 中文' },
        { t: '日本語 (Japanese)', u: 'ja.html', c: 'Language', color: '#EC4899', k: 'japanese 日本語' }
    ];

    /* ── 페이지 인덱스 (中文) ── */
    var PAGES_ZH = [
        { t: '工资计算器', u: 'zh.html', c: '计算器', color: '#2563EB', k: '工资 税后 实际收入 年薪 月薪 计算' },
        { t: '最低工资计算器', u: 'minimum-wage-zh.html', c: '计算器', color: '#F59E0B', k: '最低工资 时薪 兼职 打工 2026' },
        { t: '年薪对比表', u: 'salary-table-zh.html', c: '计算器', color: '#EF4444', k: '年薪 对比 比较 税后 收入表' },
        { t: '周休津贴计算器', u: 'holiday-pay-zh.html', c: '计算器', color: '#059669', k: '周休津贴 假日 补贴' },
        { t: '四大保险计算器', u: 'insurance-zh.html', c: '计算器', color: '#8B5CF6', k: '四大保险 国民年金 健康保险 雇佣保险' },
        { t: '综合所得税计算器', u: 'income-tax-zh.html', c: '计算器', color: '#F59E0B', k: '综合所得税 所得税 税金 自由职业' },
        { t: '赠与税计算器', u: 'gift-tax-zh.html', c: '计算器', color: '#059669', k: '赠与税 赠与 家族 遗产' },
        { t: '取得税计算器', u: 'acquisition-tax-zh.html', c: '计算器', color: '#EF4444', k: '取得税 房产 公寓 房屋 不动产' },
        { t: '退休金计算器', u: 'retirement-zh.html', c: '计算器', color: '#059669', k: '退休金 退职金 离职 工龄' },
        { t: '失业补助计算器', u: 'unemployment-zh.html', c: '计算器', color: '#8B5CF6', k: '失业补助 失业金 求职 补贴' },
        { t: '医疗费税额扣除计算器', u: 'medical-tax-zh.html', c: '计算器', color: '#EC4899', k: '医疗费 税额扣除 医院 医疗' },
        { t: '实费保险计算器', u: 'silbi-zh.html', c: '计算器', color: '#06B6D4', k: '实费保险 实损保险 保险 医院费' },
        // 语言切换
        { t: '한국어（韩语）', u: 'index.html', c: '语言', color: '#059669', k: 'korean 韩语 한국어' },
        { t: 'English（英语）', u: 'en.html', c: '语言', color: '#2563EB', k: 'english 英语' },
        { t: '日本語（日语）', u: 'ja.html', c: '语言', color: '#EC4899', k: 'japanese 日语 日本語' }
    ];

    /* ── 페이지 인덱스 (日本語) ── */
    var PAGES_JA = [
        { t: '給料計算機', u: 'ja.html', c: '計算機', color: '#2563EB', k: '給料 手取り 年収 月給 税引後 計算' },
        { t: '最低賃金計算機', u: 'minimum-wage-ja.html', c: '計算機', color: '#F59E0B', k: '最低賃金 時給 アルバイト パート 2026' },
        { t: '年収別手取り比較表', u: 'salary-table-ja.html', c: '計算機', color: '#EF4444', k: '年収 比較 一覧 手取り表' },
        { t: '週休手当計算機', u: 'holiday-pay-ja.html', c: '計算機', color: '#059669', k: '週休手当 休日 手当' },
        { t: '四大保険計算機', u: 'insurance-ja.html', c: '計算機', color: '#8B5CF6', k: '四大保険 国民年金 健康保険 雇用保険' },
        { t: '総合所得税計算機', u: 'income-tax-ja.html', c: '計算機', color: '#F59E0B', k: '総合所得税 所得税 税金 フリーランス' },
        { t: '贈与税計算機', u: 'gift-tax-ja.html', c: '計算機', color: '#059669', k: '贈与税 贈与 家族 相続' },
        { t: '取得税計算機', u: 'acquisition-tax-ja.html', c: '計算機', color: '#EF4444', k: '取得税 不動産 マンション 住宅' },
        { t: '退職金計算機', u: 'retirement-ja.html', c: '計算機', color: '#059669', k: '退職金 退職 離職 勤続年数' },
        { t: '失業給付計算機', u: 'unemployment-ja.html', c: '計算機', color: '#8B5CF6', k: '失業給付 失業手当 求職 給付金' },
        { t: '医療費税額控除計算機', u: 'medical-tax-ja.html', c: '計算機', color: '#EC4899', k: '医療費 税額控除 病院 医療' },
        { t: '実費保険計算機', u: 'silbi-ja.html', c: '計算機', color: '#06B6D4', k: '実費保険 実損保険 保険 病院費' },
        // 言語切替
        { t: '한국어（韓国語）', u: 'index.html', c: '言語', color: '#059669', k: 'korean 韓国語 한국어' },
        { t: 'English（英語）', u: 'en.html', c: '言語', color: '#2563EB', k: 'english 英語' },
        { t: '中文（中国語）', u: 'zh.html', c: '言語', color: '#EF4444', k: 'chinese 中国語 中文' }
    ];

    /* ── 현재 언어에 맞는 인덱스 선택 ── */
    var PAGES_MAP = { ko: PAGES_KO, en: PAGES_EN, zh: PAGES_ZH, ja: PAGES_JA };
    var PAGES = PAGES_MAP[lang] || PAGES_KO;

    /* ── 오버레이 DOM 생성 ── */
    var overlay, input, results;

    function createOverlay() {
        overlay = document.createElement('div');
        overlay.className = 'search-overlay';
        overlay.innerHTML =
            '<div class="search-box">' +
                '<div class="search-input-wrap">' +
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>' +
                    '<input class="search-input" type="text" placeholder="' + ui.placeholder + '" autocomplete="off">' +
                '</div>' +
                '<div class="search-results"></div>' +
            '</div>';
        document.body.appendChild(overlay);

        input = overlay.querySelector('.search-input');
        results = overlay.querySelector('.search-results');

        // 배경 클릭 시 닫기
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) closeSearch();
        });

        // 입력 이벤트
        input.addEventListener('input', function() {
            doSearch(input.value.trim());
        });

        // 키보드
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') { closeSearch(); return; }
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                moveSelection(e.key === 'ArrowDown' ? 1 : -1);
                return;
            }
            if (e.key === 'Enter') {
                var active = results.querySelector('.search-result.active');
                if (active) { window.location.href = active.getAttribute('href'); }
                return;
            }
        });

        showHint();
    }

    /* ── 힌트 (검색 전) ── */
    function showHint() {
        var isMac = navigator.platform.indexOf('Mac') > -1;
        var shortcut = isMac ? '<span class="search-kbd">⌘</span><span class="search-kbd">K</span>' : '<span class="search-kbd">Ctrl</span><span class="search-kbd">K</span>';
        results.innerHTML =
            '<div class="search-hint">' +
                ui.hint +
                '<br><br><span style="font-size:0.75rem">' + shortcut + ui.hintShortcut + '</span>' +
            '</div>';
    }

    /* ── 검색 실행 ── */
    function doSearch(query) {
        if (!query) { showHint(); return; }

        var q = query.toLowerCase();
        var scored = [];

        for (var i = 0; i < PAGES.length; i++) {
            var p = PAGES[i];
            var title = p.t.toLowerCase();
            var keywords = p.k.toLowerCase();
            var score = 0;

            // 제목 완전 일치
            if (title === q) score += 100;
            // 제목 시작 일치
            else if (title.indexOf(q) === 0) score += 80;
            // 제목 포함
            else if (title.indexOf(q) > -1) score += 60;
            // 키워드 포함
            else if (keywords.indexOf(q) > -1) score += 40;
            // 숫자 검색 (연봉 금액)
            else {
                var numQ = q.replace(/[^0-9]/g, '');
                if (numQ && keywords.indexOf(numQ) > -1) score += 30;
            }

            // 개별 단어 매칭 (여러 단어 검색)
            if (score === 0 && q.indexOf(' ') > -1) {
                var words = q.split(/\s+/);
                var matched = 0;
                for (var w = 0; w < words.length; w++) {
                    if (words[w] && (title.indexOf(words[w]) > -1 || keywords.indexOf(words[w]) > -1)) {
                        matched++;
                    }
                }
                if (matched === words.length) score += 50;
                else if (matched > 0) score += matched * 15;
            }

            if (score > 0) {
                scored.push({ page: p, score: score });
            }
        }

        // 점수순 정렬
        scored.sort(function(a, b) { return b.score - a.score; });

        if (scored.length === 0) {
            results.innerHTML = '<div class="search-no-result">' + ui.noResult + '</div>';
            return;
        }

        // 카테고리별 그룹핑 (순서 유지)
        var html = '';
        var lastCat = '';
        var count = 0;
        var MAX = 15;

        for (var j = 0; j < scored.length && count < MAX; j++) {
            var pg = scored[j].page;
            if (pg.c !== lastCat) {
                lastCat = pg.c;
                html += '<div class="search-cat-label">' + pg.c + '</div>';
            }
            html += '<a class="search-result" href="' + pg.u + '">' +
                '<div class="search-result-dot" style="background:' + pg.color + '"></div>' +
                '<div class="search-result-title">' + highlightMatch(pg.t, q) + '</div>' +
                '<div class="search-result-cat">' + pg.c + '</div>' +
                '</a>';
            count++;
        }

        if (scored.length > MAX) {
            html += '<div class="search-hint" style="padding:12px 20px;font-size:0.78rem;">' + (scored.length - MAX) + ui.more + '</div>';
        }

        results.innerHTML = html;
    }

    /* ── 검색어 하이라이트 ── */
    function highlightMatch(text, query) {
        var idx = text.toLowerCase().indexOf(query.toLowerCase());
        if (idx === -1) return text;
        return text.substring(0, idx) +
            '<strong style="color:var(--accent)">' + text.substring(idx, idx + query.length) + '</strong>' +
            text.substring(idx + query.length);
    }

    /* ── 키보드 화살표 이동 ── */
    function moveSelection(dir) {
        var items = results.querySelectorAll('.search-result');
        if (!items.length) return;

        var current = -1;
        for (var i = 0; i < items.length; i++) {
            if (items[i].classList.contains('active')) { current = i; break; }
        }

        if (current > -1) items[current].classList.remove('active');

        var next = current + dir;
        if (next < 0) next = items.length - 1;
        if (next >= items.length) next = 0;

        items[next].classList.add('active');
        items[next].scrollIntoView({ block: 'nearest' });
    }

    /* ── 열기 / 닫기 ── */
    window.openSearch = function() {
        if (!overlay) createOverlay();
        overlay.classList.add('open');
        input.value = '';
        showHint();
        setTimeout(function() { input.focus(); }, 50);
    };

    function closeSearch() {
        if (overlay) overlay.classList.remove('open');
    }

    /* ── 키보드 단축키: Ctrl+K / Cmd+K ── */
    document.addEventListener('keydown', function(e) {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            if (overlay && overlay.classList.contains('open')) {
                closeSearch();
            } else {
                openSearch();
            }
        }
        if (e.key === 'Escape' && overlay && overlay.classList.contains('open')) {
            closeSearch();
        }
    });

})();
