# Thin Content Audit — salarykorea.site

> 측정일: 2026-04-18
> 측정 방법: `<body>` 블록에서 `<script>/<style>` 제거 후 남은 텍스트 길이(공백 포함)
> 한글 char = `[가-힣]` 정규식 매치 수

## 표 (대표 17개 페이지)

| # | 페이지 | 유형 | 본문(chars) | 한글(chars) | FAQPage | 고유성 점수(1~5) | 보강 필요 | 판정 |
|---|---|---|---|---|---|---|---|---|
| 1 | income-tax.html | 계산기(메인) | 4453 | 2725 | O | 4 | - | ✅ |
| 2 | retirement.html | 계산기 | 4238 | 2732 | O | 4 | - | ✅ |
| 3 | unemployment.html | 계산기 | 3799 | 2444 | O | 3 | - | ✅ |
| 4 | minimum-wage.html | 계산기 | 3819 | 2291 | O | 3 | - | ✅ |
| 5 | holiday-pay.html | 계산기 | 3662 | 2344 | O | 3 | - | ✅ |
| 6 | insurance.html | 계산기 | 3431 | 2148 | O | 3 | - | ✅ |
| 7 | salary-table.html | 계산기 | 3403 | 2176 | O | 3 | - | 🟡 경계 |
| 8 | freelancer-tax.html | 계산기 | 3217 | 2103 | O | 4 | - | 🟡 경계 |
| 9 | gift-tax.html | 계산기 | 2838 | 1832 | **X** | 3 | FAQ 추가 | 🟡 경계 |
| 10 | monthly-salary.html | 계산기 | 2725 | 1466 | **X** | 3 | FAQ + 본문 | 🟡 경계 |
| 11 | acquisition-tax.html | 계산기 | 2612 | 1756 | **X** | 3 | FAQ + 본문 | 🟡 경계 |
| 12 | year-end-tax.html | 계산기 | 2286 | 1457 | O | 3 | +1500자 본문 | 🔴 부족 |
| 13 | silbi.html | 계산기 | 2100 | 1258 | O | 3 | +1800자 본문 | 🔴 부족 |
| 14 | index.html | 홈 | 2097 | 1344 | - | 3 | 홈 소개/가치 | 🔴 부족 |
| 15 | medical-tax.html | 계산기 | 1953 | 1272 | O | 3 | +2000자 본문 | 🔴 최우선 |
| 16 | about.html | 법적 | 2823 | - | - | 4 | - | ✅ |
| 17 | contact.html | 법적 | 1582 | - | - | 4 | - | 🟡 연락처 특수 |

## 고유성 평가 기준 (1~5)

- 1: 다른 사이트 복붙 수준 / 단순 정의만
- 2: 정의 + 얕은 안내
- 3: 정의 + FAQ + 예시 조금 (평균적)
- 4: 정의 + FAQ + 예시 + 절세/실전 가이드 + 출처
- 5: + 작성자 전문성 근거 + 법령 · 사례 연구

## 법적 필수 페이지 체크

| 페이지 | 상태 | 문제점 |
|---|---|---|
| privacy.html | ✅ | 양호 |
| about.html | ✅ | 양호 |
| contact.html | ✅ | 1582자로 짧지만 목적 상 OK |
| **terms.html** | ❌ 누락 | **AdSense 재심사 전 필수 생성** |

## 정책 위반 후보 / 리스크

1. **기계 번역 가능성 — i18n 40개 페이지**
   - `acquisition-tax-en/ja/zh`, `gift-tax-en/ja/zh` 등 각 언어별 약 10개씩
   - 한국어 원본을 대량 자동 번역했을 가능성 — 품질 미검증
   - **대응 (MANUAL_ACTIONS #8):** `noindex` 처리 또는 번역 개선
2. **"이 계산기는 ~입니다" 류 boilerplate 서두 일부 계산기에서 발견 가능성** — 페이지별 점검 필요
3. **자동 생성된 job-*.html 13개, salary-*.html 16개, company-*.html 8개**
   - 템플릿 기반일 가능성 — 본문 길이·고유성 미측정 (이번 세션 범위 외)
   - Phase 3 확장 작업으로 후속 세션에 측정 권장

## 즉시 실행 대상 (Phase 3 우선)

1. `terms.html` 신규 생성 → 전 페이지 헤더/푸터 링크 삽입
2. `medical-tax.html` 본문 +2000자 보강
3. `silbi.html` 본문 +1800자 보강
4. `year-end-tax.html` 본문 +1500자 보강
5. `gift-tax.html`, `monthly-salary.html`, `acquisition-tax.html` FAQ 섹션 추가 (FAQPage JSON-LD 포함)
6. `index.html` 홈 본문 보강 (사이트 가치 제안 + 대표 계산기 설명)
7. 모든 한국어 계산기 14개에 `작성자 + 최종 업데이트 날짜 + 출처 링크` 표준 블록 통일
