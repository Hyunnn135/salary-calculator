/* ═══════════════════════════════════════════════════════════════
 * ads.js — Alternative monetization loader (AdFit / Coupang Partners)
 *
 * PURPOSE
 *   AdSense 재승인 실패 시나리오 대비용 자리마련 파일.
 *   실제 계정 발급 전까지는 no-op로 동작하며, 슬롯 ID만 교체하면
 *   즉시 광고가 뜨도록 설계됨.
 *
 * HOW TO ACTIVATE (현태 수동 작업)
 *   1. https://adfit.kakao.com 가입 → 매체 등록 → salarykorea.site 승인
 *   2. 승인 완료 시 본 파일 최상단의 ADFIT_UNIT_ID_* 상수 교체
 *   3. 삽입 원하는 페이지에 <ins class="kakao_ad_area" ...></ins> 추가
 *   4. 이 파일을 common.js 아래 또는 body 끝에서 defer 로 로드
 *
 * CURRENT STATE: 슬롯 ID 모두 PLACEHOLDER. 로드돼도 아무 요청 안 감.
 * ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // TODO: ADFIT_UNIT_ID — 카카오 애드핏 매체 승인 후 실제 unit id 로 교체
  const ADFIT_UNIT_ID_TOP = 'TODO_ADFIT_UNIT_ID_TOP';       // 상단 배너 (728x90 또는 320x100)
  const ADFIT_UNIT_ID_MIDDLE = 'TODO_ADFIT_UNIT_ID_MIDDLE'; // 본문 중간 (300x250)
  const ADFIT_UNIT_ID_BOTTOM = 'TODO_ADFIT_UNIT_ID_BOTTOM'; // 하단 (300x250)

  // TODO: COUPANG_PARTNER_ID — 쿠팡파트너스 가입 후 ID 교체
  const COUPANG_PARTNER_ID = 'TODO_COUPANG_PARTNER_ID';

  const isPlaceholder = (v) => !v || v.indexOf('TODO_') === 0;

  // AdFit 스크립트 지연 로드 (실제 unit id가 하나라도 세팅됐을 때만)
  function loadAdFitScript() {
    if (window.__adfitLoaded) return;
    if (
      isPlaceholder(ADFIT_UNIT_ID_TOP) &&
      isPlaceholder(ADFIT_UNIT_ID_MIDDLE) &&
      isPlaceholder(ADFIT_UNIT_ID_BOTTOM)
    ) {
      return; // 아직 승인 전 — 요청 발생 안 시킴
    }
    const s = document.createElement('script');
    s.src = '//t1.daumcdn.net/kas/static/ba.min.js';
    s.async = true;
    document.head.appendChild(s);
    window.__adfitLoaded = true;
  }

  // 페이지에 정의된 슬롯 div 에 AdFit ins 태그를 주입
  function mountAdFitSlots() {
    const slots = [
      { sel: '[data-ad-slot="top"]', id: ADFIT_UNIT_ID_TOP, w: 728, h: 90 },
      { sel: '[data-ad-slot="middle"]', id: ADFIT_UNIT_ID_MIDDLE, w: 300, h: 250 },
      { sel: '[data-ad-slot="bottom"]', id: ADFIT_UNIT_ID_BOTTOM, w: 300, h: 250 }
    ];
    slots.forEach(({ sel, id, w, h }) => {
      if (isPlaceholder(id)) return;
      document.querySelectorAll(sel).forEach((host) => {
        if (host.dataset.adfitMounted) return;
        const ins = document.createElement('ins');
        ins.className = 'kakao_ad_area';
        ins.style.display = 'none';
        ins.setAttribute('data-ad-unit', id);
        ins.setAttribute('data-ad-width', String(w));
        ins.setAttribute('data-ad-height', String(h));
        host.appendChild(ins);
        host.dataset.adfitMounted = '1';
      });
    });
  }

  // 쿠팡파트너스 위젯 슬롯 (옵션)
  function mountCoupangSlots() {
    if (isPlaceholder(COUPANG_PARTNER_ID)) return;
    // 쿠팡파트너스는 매체별 위젯 iframe URL을 개별 발급받아야 하므로
    // 위젯별 src를 HTML 측에 직접 삽입하는 방식이 더 안전함. 여기서는 no-op.
  }

  function init() {
    loadAdFitScript();
    mountAdFitSlots();
    mountCoupangSlots();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
