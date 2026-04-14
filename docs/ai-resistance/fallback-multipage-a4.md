# [Fallback] 옵션 2 — A4 다중 페이지, 블록 단위 분할

> 상태: 대기 (2026-04-14 기준 단일 긴 페이지 방식 ①로 진행 중)
> 발동 조건: ①이 실사용에서 문제가 드러나는 경우 (예: 긴 PDF가 특정 뷰어에서 잘리거나, 인쇄 시 축소 품질이 안 좋음, 사용자가 "A4 인쇄용"을 명시 요청)
> 관련 파일: `trust-layer.js` → `saveAsPDF()`

---

## 🎯 목표

A4 다중 페이지를 쓰되 페이지 경계에서 콘텐츠가 행/문자 단위로 잘리지 않도록, **블록 단위(행·카드 단위) 로 안전한 페이지 분할**을 구현.

---

## 🧭 접근 방식 3가지

### (A) DOM 블록 개별 캡처 후 조립 — 가장 깔끔, 가장 복잡

`captureTarget`의 top-level 블록을 하나씩 개별 canvas로 캡처한 뒤 jsPDF 페이지에 이어 붙이는 방식.

```
1. 블록 목록: [capture-header, capture-trust-badge, capture-meta, result-hero,
   breakdown-card, bookkeeping-card, capture-footer]
2. 각 블록을 html2canvas로 개별 캡처 (clone 오버헤드 N배 발생)
3. PDF 페이지 생성 루프:
   - 현재 페이지 남은 공간 ≥ 블록 높이 → 현재 페이지에 추가
   - 부족하면 addPage() 후 새 페이지에 추가
   - 단일 블록이 A4 한 페이지보다 큰 경우(예: breakdown-card가 길면)
     → 내부 행 단위로 한 번 더 분할 필요
```

**장점:** 페이지 경계에서 절대 잘리지 않음. 인쇄 결과가 프로페셔널.
**단점:** html2canvas 호출 N번 (캡처 시간 3~5배 증가 예상). 단일 블록이 너무 긴 경우 내부 분할 로직 추가 필요.

### (B) 한 번 캡처 + 좌표 기반 슬라이싱 — 중간 복잡도

전체 `captureTarget`을 한 번에 캡처한 뒤, 각 블록의 DOM 위치(`getBoundingClientRect`)를 기반으로 canvas를 safe break point에서 슬라이스.

```
1. captureTarget 한 번 캡처 (기존과 동일)
2. 각 top-level 블록의 Y 좌표 범위 수집:
   blocks = [
     { top: 0,    bottom: 80,   name: 'header' },
     { top: 80,   bottom: 140,  name: 'trust-badge' },
     { top: 140,  bottom: 300,  name: 'meta' },
     ...
   ]
3. 페이지 단위 슬라이스:
   - 페이지 하단 Y = pageNumber * pageHeightInCanvas
   - 이 Y 위에 걸린 블록을 찾아 → 블록 시작점을 안전 분할점으로 선택
   - 분할점까지만 슬라이스해서 페이지에 추가
4. 남은 부분을 다음 페이지로 계속
```

**장점:** html2canvas 1회만 호출. 속도 합리적.
**단점:** 좌표 계산이 devicePixelRatio / scale 요인과 엮여서 디버깅 까다로움. 단일 블록이 페이지보다 크면 여전히 그 블록은 내부에서 잘림.

### (C) CSS `page-break-inside: avoid` 유사 방식 — 가장 가벼움

각 블록에 페이지 번호 힌트(class `.page-break-before`)를 붙여 강제로 페이지 분할 지점을 지정. 캡처는 블록별로 나눠서 한다.

```html
<div id="captureTarget">
    <div class="capture-block">
        <div class="capture-header-clone">...</div>
        <div class="capture-trust-badge">...</div>
        <div class="capture-meta">...</div>
    </div>
    <div class="capture-block">
        <div class="result-hero">...</div>
    </div>
    <div class="capture-block">
        <div class="breakdown-card">...</div>
    </div>
    <div class="capture-block">
        <div class="bookkeeping-card">...</div>
        <div class="capture-footer-clone">...</div>
    </div>
</div>
```

**장점:** 구조적으로 명확. 디자이너 친화적.
**단점:** 수동 그룹핑. 각 블록 그룹 높이가 A4를 초과하면 여전히 잘림.

---

## 🏆 추천 구현 순서

①이 실전 배포 후 사용자 피드백을 받은 시점에 이 문서 다시 열기.

1. **먼저 (B)로 프로토타입**: 한 번 캡처 + 좌표 슬라이싱. 속도 대비 품질 트레이드오프가 가장 좋음.
2. (B)에서 "단일 블록이 페이지보다 큰 경우"가 실제로 발생하면 → 해당 블록만 (A)로 보강.
3. (C)는 각 페이지의 반복 헤더(예: 페이지 하단에 "월급연구소 · 페이지 N/M")를 넣고 싶을 때 추가 검토.

---

## 📐 페이지 헤더·푸터 (다중 페이지 방식 필수 요소)

다중 페이지로 가면 현재의 "맨 위 1회 헤더, 맨 아래 1회 푸터" 구조로는 부족함:

- **모든 페이지 상단**: 작은 브랜드 로고 + 계산기명 (반복)
- **모든 페이지 하단**: 페이지 번호 `1/3`, 생성일자, 짧은 URL
- **첫 페이지만**: 풀헤더 + Trust Badge + 입력 메타
- **마지막 페이지만**: 참고자료 + 면책 푸터

이 부분은 jsPDF의 `setPage()` + `text()` 조합으로 처리 (각 페이지 루프에서 직접 그리기).

---

## 🚨 ①에서 ②로 전환할 때 체크리스트

- [ ] ①의 PDF를 실제로 공유받은 사람들이 "너무 길다"고 느끼는지 확인
- [ ] 모바일 뷰어(카톡 내장, 네이버 메일 등)에서 ①의 긴 페이지가 정상 렌더되는지 확인
- [ ] 인쇄 시 ①의 "페이지에 맞춤" 자동 축소 결과가 실용적으로 읽히는지 확인
- [ ] 위 중 하나라도 실패 → (B) 프로토타입으로 전환
