# MANUAL_ACTIONS — 현태 직접 수행 필수 작업

> 이 파일에 있는 항목은 Claude가 자동 실행하지 않은 / 실행 금지된 작업입니다.
> **모든 후속 작업은 이 파일만 보면 정리됩니다.**
> 세션 시작: 2026-04-18

---

## 우선순위

| # | 작업 | 예상 소요 | 언제 | 의존성 |
|---|---|---|---|---|
| 1 | git add/commit/push | 5분 | **지금 바로** | - |
| 2 | 배포 확인 (GitHub Pages 반영) | 2분 | push 후 | 1 의존 |
| 3 | 배포된 페이지에서 3버튼 수동 테스트 (PDF/이미지/링크) | 5분 | 배포 후 | 2 의존 |
| 4 | 카카오 AdFit 계정 생성 + 매체 등록 | 15분 | 오늘 내 | - |
| 5 | AdFit 광고 단위 ID 발급 후 코드에 교체 | 5분 | 4 의존 | 4 의존 |
| 6 | 쿠팡 파트너스 가입 + 트래킹 링크 발급 | 20분 | 선택 | - |
| 7 | AdSense 재검토 요청 | 1분 | **1~5 전부 완료 후** | 1,2,3 필수 |
| 8 | i18n 페이지 (`-en/-ja/-zh`) 품질 검토 or noindex | 30분+ | 7 전/후 선택 | - |
| 9 | 구글 색인 재요청 (보강된 계산기 3개 URL) | 5분 | 배포 후 | 2 의존 |

---

## 1. git 푸시 (5분 · 지금 바로)

- **왜 필요한가:** Claude가 자동 push를 하지 않음. WORKFLOW_RULES 2번에 따라 통합 프롬프트를 아래에 제공함.
- **언제:** 지금
- **정확한 명령어:**
  ```bash
  cd ~/Desktop/Projects/salarykorea
  git status
  git add .
  git commit -m "feat: AdSense 재심사 대비 - terms 신규, thin content 보강, 수익화 슬롯 준비"
  git push origin main
  ```
- **관련 파일:** 아래 "수정 파일 목록" 참조
- **예상 소요 시간:** 5분

### VS Code Claude 전달용 통합 프롬프트

```
📌 [VS Code Claude 전달용 프롬프트]
프로젝트: salarykorea
변경 파일: (아래 수정 파일 목록 참조)
요약: AdSense 재심사 대비 — terms 신규 · 얇은 콘텐츠 페이지 보강 · 수익화 슬롯 자리 마련 · 작성자/업데이트 메타 추가

→ 다음 명령을 실행해줘:
cd ~/Desktop/Projects/salarykorea
git add .
git commit -m "feat: AdSense 재심사 대비 - terms 신규, thin content 보강, 수익화 슬롯 준비"
git push origin main
```

---

## 2. 배포 확인 (2분)

- **왜 필요한가:** GitHub Pages 자동 배포 완료 후에만 AdSense 재검토 요청 의미 있음
- **언제:** git push 1~3분 후
- **정확한 경로:**
  1. https://salarykorea.site/terms 접속 → 새 페이지 정상 표시 확인
  2. https://salarykorea.site/medical-tax 접속 → 보강된 본문 확인
  3. https://salarykorea.site/silbi 접속 → 보강된 본문 확인
  4. 헤더/푸터에 "이용약관" 링크 새로 표시되는지 확인
- **예상 소요 시간:** 2분

---

## 3. 3버튼 (PDF/이미지/링크) 수동 테스트 (5분)

- **왜 필요한가:** 이전 세션에서 "수정할 게 너무 많다"며 종료한 부분. 코드 리뷰 상 로직은 견고하나 실제 사용자 체감 이슈는 실기기에서만 확인 가능.
- **언제:** 배포 확인 후
- **정확한 경로:**
  1. PC에서 https://salarykorea.site/income-tax 접속
  2. 값 입력 후 계산 → 결과 하단 3버튼 클릭
  3. 각 버튼별 확인 항목:
     - PDF 저장: 파일명 `종합소득세_계산결과_20260418.pdf` 형식 / 페이지 잘림 없음 / 헤더·Trust Badge·푸터 포함
     - 이미지 저장: PNG 파일 저장 / 해상도 선명함 / 하단 참고자료 표시됨
     - 링크 복사: 토스트 "링크가 복사되었어요" / URL 파라미터에 입력값 포함
  4. 모바일 iOS Safari에서 동일 테스트 (특히 PDF 저장이 iOS에서 새 탭으로 뜨는지)
  5. 불편한 부분 메모해서 다음 세션에 공유
- **관련 파일:** `trust-layer.js`, `common.css`, 적용된 4개 계산기(income-tax, freelancer-tax, year-end-tax, medical-tax)
- **예상 소요 시간:** 5분

**Claude 판단:** 코드상 3버튼 구조는 합리적이라 자동 수정 대상이 아님. **체감 이슈 목록을 받은 뒤** 해당 부분만 수정하는 것이 효율적이므로 이번 세션에서는 자동 수정 보류. (MANUAL_ACTIONS.md에만 기록)

---

## 4. 카카오 AdFit 계정 생성 (15분 · 오늘 내)

- **왜 필요한가:** AdSense 재심사 결과 대기 동안 대체 수익화 가동. 국내 1인 개발자 진입 가장 낮음.
- **언제:** 오늘 안
- **정확한 경로:**
  1. https://adfit.kakao.com/ 접속
  2. "매체 등록하기" → 카카오 로그인
  3. 사이트 등록: 사이트명 "월급연구소", URL `https://salarykorea.site`, 카테고리 "금융/재테크"
  4. 심사 2~3일 대기 (AdSense와 달리 까다롭지 않음)
  5. 승인 후 "광고단위 관리" → 광고단위 생성
     - 사이즈 추천: 320x100 (모바일 inline), 728x90 (PC 가로), 250x250 (사이드/컨텐츠)
  6. 발급받는 정보: 매체 ID (8자리), 광고단위 ID (`DAN-xxxx` 형식)
- **관련 파일:** 아래 5번에서 교체
- **예상 소요 시간:** 초기 가입 15분 + 심사 대기 2~3일

---

## 5. AdFit 광고 단위 ID 코드 교체 (5분)

- **왜 필요한가:** 자동 실행 금지 항목. 실제 키 노출 방지
- **언제:** 4번 승인 후
- **정확한 작업:**
  1. 파일 열기: `~/Desktop/Projects/salarykorea/ads.js` (이번 세션에서 신규 생성)
  2. `TODO: ADFIT_UNIT_ID` 주석을 발급받은 광고단위 ID로 교체
  3. 광고 슬롯이 들어간 페이지 목록은 `AUTO_SESSION_REPORT.md`의 "3-B. 광고 슬롯 삽입 페이지" 참고
  4. VS Code Claude에 "AdFit 광고단위 ID 교체 + git push" 프롬프트 전달
- **관련 파일:** `assets/js/ads.js`, 광고 슬롯 삽입된 계산기 페이지들
- **예상 소요 시간:** 5분

---

## 6. 쿠팡 파트너스 (선택 · 20분)

- **왜 필요한가:** 세무 관련 도서 / 가계부 / 휴대용 프린터(영수증 인쇄) 제휴로 보완
- **언제:** 여유 있을 때
- **정확한 경로:**
  1. https://partners.coupang.com/ 가입
  2. 승인 후 "상품 링크" → 검색: "세무", "가계부", "절세 가이드북"
  3. 추천 상품 5~10개 큐레이션 → 마크다운으로 목록 저장 (Claude가 다음 세션에 HTML 삽입)
  4. `"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."` 문구 페이지별 필수
- **관련 파일:** 아직 없음. 다음 세션에서 추천 페이지 생성
- **예상 소요 시간:** 20분

---

## 7. AdSense 재검토 요청 (1분 · 1~5 완료 후)

- **왜 필요한가:** 자동 실행 금지. 반드시 현태가 직접 버튼 클릭.
- **언제:** **반드시** 1번 push + 2번 배포 확인 + 3번 수동 테스트 완료 후
- **정확한 경로:**
  1. https://www.google.com/adsense/ 접속 → 로그인
  2. 사이트 → salarykorea.site 선택
  3. "정책 센터" 또는 "사이트 > 검토 요청"
  4. "문제를 수정했음을 확인함" 체크
  5. "검토 요청" 버튼 클릭
  6. 결과 대기: 2~14일
- **주의:** 배포 반영되지 않은 상태에서 요청하면 동일 사유로 재거절 가능
- **예상 소요 시간:** 1분 (대기 기간 제외)

---

## 8. i18n 페이지 (-en/-ja/-zh) 품질 검토 or noindex (30분+ · 선택)

- **왜 필요한가:** 기계 번역 기반이면 thin content 리스크. AdSense는 주 언어 기준 품질 평가 가능
- **언제:** 7번 결과 나오기 전후 선택
- **옵션 A (추천):** 번역 품질 확인 → 낮으면 `<meta name="robots" content="noindex">` 일괄 추가
- **옵션 B:** DeepL/ChatGPT로 번역 개선 (시간 多)
- **관련 파일:** 40개 `*-en.html`, `*-ja.html`, `*-zh.html` + en.html, ja.html, zh.html
- **Claude 체크:** 자동으로 `noindex` 추가하려면 말씀 부탁. 번역 품질을 제가 판정할 수 없어 기본 대기.
- **예상 소요 시간:** 30분~3시간

---

## 9. 구글 색인 재요청 (5분)

- **왜 필요한가:** 본문 크게 바꾼 페이지는 재색인해야 AdSense 검토 시 최신 버전 평가
- **언제:** 2번 배포 확인 후
- **정확한 명령어:**
  ```bash
  cd ~/Desktop/Projects/salarykorea
  python3 tools/index-submit.py \
    --urls https://salarykorea.site/medical-tax \
    https://salarykorea.site/silbi \
    https://salarykorea.site/year-end-tax \
    https://salarykorea.site/terms \
    https://salarykorea.site/
  ```
  (실제 스크립트 인자는 `tools/index-submit.py --help` 확인)
- **관련 파일:** `tools/index-submit.py`
- **예상 소요 시간:** 5분

---

## 수정 파일 목록 (git push용)

### 신규 파일 (2개)
- `terms.html` — 이용약관 11조 (신규 작성, 본문 ~3.6k자)
- `ads.js` — AdFit/Coupang 광고 로더 스텁 (placeholder 상태)

### 본문 대폭 보강 (4개)
- `medical-tax.html` — 본문 1953 → 4225자
- `silbi.html` — 본문 2100 → 4236자
- `year-end-tax.html` — 본문 2286 → 4283자
- `index.html` — 본문 2097 → 3200자+ (홈 소개 확장)

### FAQPage JSON-LD + canonical 추가 (3개)
- `gift-tax.html`
- `acquisition-tax.html`
- `monthly-salary.html`

### 전역 푸터 일괄 업데이트 (105개)
- 전 HTML 파일에 `terms.html` 푸터 링크 주입 (한국어 69 + en 12 + ja 11 + zh 12 + 기타 1)

### SEO (1개)
- `sitemap.xml` — `/terms`, `/year-end-tax` 신규 URL 추가, 6개 페이지 `lastmod` 2026-04-18 갱신

### 보고·계획 파일
- `AUTO_SESSION_REPORT.md` — 세션 전체 로그
- `thin_content_audit.md` — Phase 1 진단 결과
- `MANUAL_ACTIONS.md` — 이 파일

---

## 수정 파일 경로 전체 (한 줄 요약)

```
terms.html ads.js medical-tax.html silbi.html year-end-tax.html index.html
gift-tax.html acquisition-tax.html monthly-salary.html sitemap.xml
AUTO_SESSION_REPORT.md thin_content_audit.md MANUAL_ACTIONS.md
+ 전체 105개 HTML footer (terms 링크 주입)
```

---

## 참고: 자동 실행 금지 목록 (이번 세션 내)

- git add/commit/push — 위 1번 참조
- AdSense 재검토 요청 — 위 7번 참조
- 외부 계정 신규 생성 (AdFit, 쿠팡 파트너스) — 위 4, 6번 참조
- API 키·광고 슬롯 ID 코드 삽입 — 위 5번 참조 (placeholder만 넣음)
- 도메인·호스팅·DNS 변경
- 블로그 별도 프로젝트 신규 생성 또는 기존 블로그 건드리기
- 다른 프로젝트(realestate, maxout, nudge) 파일 수정
- 배포 직접 실행
