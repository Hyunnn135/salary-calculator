# AI 내성 레이어 공통 컴포넌트 설계서

> **목적:** 계산기 페이지에 삽입할 3축 컴포넌트의 **재사용 가능한 HTML/CSS/JS 스펙**.
> **적용 방법:** `common.css`에 스타일 추가 + `trust-layer.js` 단일 파일 로드 → 페이지당 3줄 삽입으로 활성화.
> **파일럿 적용 전에 현태님 컨펌 필요.**

---

## 1. 컴포넌트 A — Trust Badge (상단 검증 배지)

### HTML
```html
<div class="trust-badge">
  <span class="trust-badge-dot"></span>
  <strong>2026년 개정 세법 기준</strong>
  <span class="trust-badge-sep">·</span>
  <span>최종 업데이트 2026.04.14</span>
  <a href="/about#verification" class="trust-badge-link" aria-label="검증 방법 보기">ⓘ</a>
</div>
```

### 배치
- 계산기 페이지의 **페이지 제목(h1) 바로 아래**
- 홈 랜딩에서는 각 계산기 카드 하단에 축약형(`trust-badge--compact`)

### CSS 추가 (common.css)
```css
.trust-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #065F46;
  margin: 8px 0 16px;
  letter-spacing: -0.2px;
}
.trust-badge-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 0 2px rgba(16,185,129,0.2);
}
.trust-badge-sep { color: #6EE7B7; }
.trust-badge-link {
  margin-left: 4px;
  color: #047857;
  text-decoration: none;
  font-weight: 700;
}
.trust-badge-link:hover { text-decoration: underline; }

/* 모바일 축약 */
@media (max-width: 480px) {
  .trust-badge { font-size: 0.72rem; padding: 5px 10px; }
}
```

---

## 2. 컴포넌트 B — Result Actions (결과 저장/공유 버튼 그룹)

### HTML
```html
<div class="result-actions" id="resultActions" hidden>
  <button type="button" class="ra-btn" data-action="save-pdf">
    <svg aria-hidden="true" width="16" height="16">…</svg>
    PDF로 저장
  </button>
  <button type="button" class="ra-btn" data-action="save-image">
    이미지로 저장
  </button>
  <button type="button" class="ra-btn" data-action="share-link">
    결과 링크 복사
  </button>
  <button type="button" class="ra-btn ra-btn--ghost" data-action="print">
    인쇄
  </button>
</div>
```

### 배치
- 결과가 렌더링된 카드(.result-hero) 바로 아래
- 계산이 실행되면 JS가 `hidden` 속성 제거

### CSS
```css
.result-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed var(--border);
}
.ra-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.15s;
}
.ra-btn:hover {
  border-color: var(--accent);
  background: #F0F9FF;
}
.ra-btn--ghost { background: transparent; color: var(--text-secondary); }
```

### JS 바인딩 규약
- `data-action` 속성으로 dispatch
- 결과 DOM의 루트는 `id="captureTarget"`로 약속 (페이지별로 통일)
- 각 페이지 공통 부트스트랩:
  ```html
  <script src="/trust-layer.js" defer></script>
  <script>
    window.addEventListener("DOMContentLoaded", () => {
      window.TrustLayer.bind({
        targetId: "captureTarget",
        filename: "종합소득세_계산결과",   // 페이지별 커스터마이즈
        shareParams: () => collectInputs()  // 페이지별 함수
      });
    });
  </script>
  ```

---

## 3. 컴포넌트 C — Sources Footer (출처·근거 박스)

### HTML
```html
<section class="sources-footer" aria-label="계산 근거 및 출처">
  <h3 class="sources-title">📚 이 계산의 근거</h3>
  <ul class="sources-list">
    <li>
      <strong>소득세법 제55조 (세율)</strong>
      <span>— 2026년 개정 기준 8구간 누진세율 적용</span>
      <a href="https://www.law.go.kr/…" target="_blank" rel="noopener">원문 보기</a>
    </li>
    <li>
      <strong>국민연금공단 2026 기준소득월액</strong>
      <span>상한 617만원 / 하한 39만원</span>
      <a href="https://www.nps.or.kr/…" target="_blank" rel="noopener">공식 자료</a>
    </li>
    <li>
      <strong>건강보험공단 2026 보험료율</strong>
      <span>7.09% (장기요양보험료 별도)</span>
      <a href="https://www.nhis.or.kr/…" target="_blank" rel="noopener">공식 자료</a>
    </li>
  </ul>
  <p class="sources-note">
    ⚠️ 본 계산기는 일반적인 경우에 기반합니다. 개인 상황(부양가족, 추가 공제 등)에 따라
    실제 금액은 달라질 수 있으며, 중요한 의사결정 전에는 세무사 상담을 권장합니다.
  </p>
  <p class="sources-changelog">
    최근 반영 내역: 2026.01.01 소득세 구간 조정 · 2026.01.01 국민연금 상한 인상
  </p>
</section>
```

### 배치
- 계산기 결과 영역 **바로 아래**, 관련 링크 카드 **위**

### CSS
```css
.sources-footer {
  margin: 32px 0;
  padding: 24px;
  background: #F9FAFB;
  border: 1px solid var(--border);
  border-radius: 16px;
}
.sources-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 14px;
}
.sources-list {
  list-style: none;
  padding: 0;
  margin: 0 0 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sources-list li {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
}
.sources-list strong { color: var(--text-primary); }
.sources-list a {
  margin-left: 6px;
  color: var(--accent);
  font-size: 0.78rem;
}
.sources-note {
  font-size: 0.8rem;
  color: var(--text-tertiary);
  background: #FEF3C7;
  border-left: 3px solid #F59E0B;
  padding: 10px 12px;
  border-radius: 6px;
  margin: 0 0 10px;
  line-height: 1.5;
}
.sources-changelog {
  font-size: 0.72rem;
  color: var(--text-tertiary);
  margin: 0;
  font-style: italic;
}
```

---

## 4. trust-layer.js (공통 JS 유틸 스펙)

### 파일 위치
`/trust-layer.js` (사이트 루트)

### 의존 CDN
- `html2canvas` (이미지 캡처)
- `jsPDF` (PDF 변환)
- 둘 다 **lazy-load**: 버튼 클릭 시에만 동적 import

### API
```js
window.TrustLayer = {
  /**
   * 페이지에 Result Actions 버튼 바인딩
   * @param {object} opts
   * @param {string} opts.targetId  - 캡처 대상 DOM id
   * @param {string} opts.filename  - 다운로드 파일명 prefix
   * @param {function} opts.shareParams - 공유 링크에 넣을 객체 반환 함수
   */
  bind(opts) { /* ... */ },

  async saveAsPDF(elementId, filename) { /* html2canvas → jsPDF */ },
  async saveAsImage(elementId, filename) { /* html2canvas → blob → download */ },
  copyShareURL(params) {
    const url = new URL(location.href);
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    navigator.clipboard.writeText(url.toString());
    // toast: "링크가 복사되었습니다"
  },
  print() { window.print(); }
};
```

### 인쇄 전용 스타일 (common.css 하단 추가)
```css
@media print {
  header, nav, .ads-slot, .result-actions, .article-card, .sources-footer a { display: none !important; }
  .trust-badge { border: 1px solid #666; color: #000; background: #fff; }
  .result-hero { background: #fff !important; color: #000 !important; box-shadow: none; border: 2px solid #000; }
}
```

---

## 5. 각 계산기 페이지 적용 패치 (3줄 삽입)

```html
<!-- 페이지 <h1> 아래 -->
<div class="trust-badge">…</div>

<!-- 결과 카드 안 -->
<div id="captureTarget">
   … 기존 결과 HTML …
   <div class="result-actions" id="resultActions" hidden>…</div>
</div>

<!-- 결과 영역 아래 -->
<section class="sources-footer">…</section>

<!-- </body> 직전 -->
<script src="/trust-layer.js" defer></script>
```

---

## 6. 파일럿 후보 & 우선순위 제안

| 페이지 | 우선순위 | 이유 |
|---|---|---|
| `income-tax.html` | ⭐ 추천 1순위 | 종합소득세, 검색량 많고 출처가 명확 (소득세법) |
| `insurance.html` | 2순위 | 4대보험 계산, 보험료율 공식 출처 깔끔 |
| `retirement.html` | 3순위 | 퇴직금 계산, 근로자퇴직급여보장법 출처 명확 |
| `year-end-tax.html` | 4순위 | 연말정산, 변수가 많아 출처 복잡 — 뒤로 미룸 |

**현태님 선택**: 파일럿 페이지를 한 개 골라주시면 다음 세션에 실제 코드 패치 들어감.

---

## 7. 롤아웃 예상 공수

| 단계 | 예상 작업 시간 |
|---|---|
| trust-layer.js + common.css 확장 | 2~3시간 |
| 파일럿 페이지 1개 패치 | 1~1.5시간 |
| 메인 계산기 14개 롤아웃 (템플릿화 후) | 페이지당 20~30분 |
| 블로그/가이드 페이지는 배지·출처만 (저장 버튼 제외) | 페이지당 5~10분 |

---

## 8. 구현 체크리스트 (다음 세션용)

```
[ ] 파일럿 페이지 컨펌 받기
[ ] common.css 에 3개 컴포넌트 스타일 추가
[ ] trust-layer.js 작성 (~150줄 예상)
[ ] 파일럿 페이지에 패치 적용
[ ] 로컬에서 PDF/이미지 저장 실제 작동 확인
[ ] 인쇄 미리보기에서 깨지는 요소 없는지 확인
[ ] Git push & 배포
[ ] 배포된 URL에서 실제 작동 검증
[ ] 현태님 피드백 → 롤아웃 진행
```
