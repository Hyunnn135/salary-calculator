/**
 * trust-layer.js
 * salarykorea — AI 내성 레이어 공통 유틸
 *
 * 기능:
 *  - PDF 저장 (html2canvas + jsPDF)
 *  - 이미지 저장 (html2canvas → PNG)
 *  - 공유 링크 복사 (URL 파라미터 인코딩)
 *  - 인쇄
 *
 * 라이브러리는 버튼 클릭 시점에 lazy-load.
 *
 * 사용법:
 *   <div class="result-actions" id="resultActions" hidden>
 *     <button class="ra-btn" data-action="save-pdf">PDF로 저장</button>
 *     <button class="ra-btn" data-action="save-image">이미지로 저장</button>
 *     <button class="ra-btn" data-action="share-link">결과 링크 복사</button>
 *     <button class="ra-btn ra-btn--ghost" data-action="print">인쇄</button>
 *   </div>
 *   <script>
 *     TrustLayer.bind({
 *       targetId: "captureTarget",
 *       filename: "종합소득세_계산결과",
 *       shareParams: () => ({ income: incomeInput.value, type: currentType })
 *     });
 *     // 계산 완료 시점에:
 *     TrustLayer.show();
 *   </script>
 */
(function (window, document) {
    "use strict";

    var HTML2CANVAS_URL = "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
    var JSPDF_URL = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js";

    var _libPromises = {};
    function loadScript(url) {
        if (_libPromises[url]) return _libPromises[url];
        _libPromises[url] = new Promise(function (resolve, reject) {
            var s = document.createElement("script");
            s.src = url;
            s.async = true;
            s.onload = resolve;
            s.onerror = function () { reject(new Error("Failed to load " + url)); };
            document.head.appendChild(s);
        });
        return _libPromises[url];
    }

    function toast(msg) {
        var t = document.querySelector(".ra-toast");
        if (!t) {
            t = document.createElement("div");
            t.className = "ra-toast";
            document.body.appendChild(t);
        }
        t.textContent = msg;
        requestAnimationFrame(function () { t.classList.add("show"); });
        clearTimeout(t._hideTimer);
        t._hideTimer = setTimeout(function () { t.classList.remove("show"); }, 2200);
    }

    function todayStr() {
        var d = new Date();
        var y = d.getFullYear();
        var m = String(d.getMonth() + 1).padStart(2, "0");
        var dd = String(d.getDate()).padStart(2, "0");
        return y + m + dd;
    }

    function setBtnBusy(btn, busy, origLabel) {
        if (!btn) return;
        if (busy) {
            btn.dataset.origLabel = btn.textContent.trim();
            btn.setAttribute("disabled", "disabled");
            btn.textContent = origLabel || "처리 중...";
        } else {
            btn.removeAttribute("disabled");
            if (btn.dataset.origLabel) {
                btn.innerHTML = btn.dataset.origLabel;
                delete btn.dataset.origLabel;
            }
        }
    }

    async function captureElement(el, scale) {
        await loadScript(HTML2CANVAS_URL);

        // 화질 향상: devicePixelRatio 고려한 실질 scale 계산.
        // 레티나: 3~4, 일반 디스플레이: 3.
        var dpr = window.devicePixelRatio || 1;
        var effectiveScale = scale || Math.max(3, Math.min(dpr * 2, 4));

        // html2canvas는 원본 DOM을 off-document에 clone해서 렌더링함.
        // clone 시점에 .show 클래스에 의해서만 display되는 요소들이 보이지 않는 문제 방지 →
        // clone된 DOM에 직접 inline style 주입해서 강제로 display 유지.
        return await window.html2canvas(el, {
            backgroundColor: "#FFFFFF",
            scale: effectiveScale,
            useCORS: true,
            logging: false,
            imageTimeout: 0,
            allowTaint: false,
            letterRendering: true,
            onclone: function (clonedDoc) {
                try {
                    // 결과 카드들: .show가 붙은 것만 display
                    var showItems = clonedDoc.querySelectorAll(
                        ".result-hero.show, .breakdown-card.show, .action-row.show"
                    );
                    showItems.forEach(function (node) {
                        node.style.display = "block";
                        node.style.visibility = "visible";
                        node.style.opacity = "1";
                        node.style.animation = "none"; // fadeUp 애니메이션 중간에 캡처되는 것 방지
                    });
                    // result-hero는 flex 자식 배치이므로 display:block보단 원래 block이 맞음.
                    // 그러나 result-hero-stats 내부는 grid 유지 필요.
                    var stats = clonedDoc.querySelectorAll(".result-hero-stats");
                    stats.forEach(function (s) {
                        s.style.display = "grid";
                    });
                    // action-row는 flex
                    var actionRow = clonedDoc.querySelector(".action-row.show");
                    if (actionRow) actionRow.style.display = "flex";
                    // 캡처 대상에 배경과 패딩을 inline으로 부여 (PDF/이미지 가장자리 여백)
                    var root = clonedDoc.getElementById(el.id);
                    if (root) {
                        root.style.background = "#FFFFFF";
                        root.style.padding = "20px";
                        root.style.borderRadius = "12px";
                        root.style.display = "block";
                    }
                    // 결과 저장 버튼·카카오 공유 버튼은 캡처 결과에서 숨김
                    var hideInCapture = clonedDoc.querySelectorAll(".result-actions, .action-row");
                    hideInCapture.forEach(function (n) { n.style.display = "none"; });
                    // 상단에 Trust Badge 복제 삽입 (캡처 결과에 검증 정보가 함께 찍히도록)
                    var badgeOrig = document.querySelector(".trust-badge");
                    if (badgeOrig && root && !root.querySelector(".trust-badge-clone")) {
                        var badgeClone = badgeOrig.cloneNode(true);
                        badgeClone.classList.add("trust-badge-clone");
                        badgeClone.style.marginBottom = "16px";
                        root.insertBefore(badgeClone, root.firstChild);
                    }
                } catch (e) {
                    console.warn("onclone 처리 중 경고:", e);
                }
            }
        });
    }

    async function saveAsPDF(targetId, filename, btn) {
        var el = document.getElementById(targetId);
        if (!el) { toast("결과 영역을 찾을 수 없어요"); return; }
        setBtnBusy(btn, true, "PDF 만드는 중...");
        try {
            var canvas = await captureElement(el);
            await loadScript(JSPDF_URL);
            var jsPDF = window.jspdf ? window.jspdf.jsPDF : window.jsPDF;
            // compress: false → PDF 내부 이미지 스트림 압축 해제로 화질 보존.
            var pdf = new jsPDF({
                orientation: "p",
                unit: "mm",
                format: "a4",
                compress: false,
                putOnlyUsedFonts: true
            });
            var pageW = pdf.internal.pageSize.getWidth();
            var pageH = pdf.internal.pageSize.getHeight();
            var imgW = pageW - 20; // 여백 10mm씩
            var imgH = (canvas.height * imgW) / canvas.width;
            var y = 10;
            // PNG + compression 'SLOW' → 최고 화질 (파일 크기 vs 화질 균형)
            var imgData = canvas.toDataURL("image/png", 1.0);
            if (imgH <= pageH - 20) {
                pdf.addImage(imgData, "PNG", 10, y, imgW, imgH, undefined, "SLOW");
            } else {
                // 세로로 긴 경우: 여러 페이지로 분할
                var remainingH = imgH;
                var offsetY = 0;
                while (remainingH > 0) {
                    pdf.addImage(imgData, "PNG", 10, y - offsetY, imgW, imgH, undefined, "SLOW");
                    remainingH -= (pageH - 20);
                    if (remainingH > 0) {
                        pdf.addPage();
                        offsetY += (pageH - 20);
                    }
                }
            }
            pdf.save(filename + "_" + todayStr() + ".pdf");
            toast("PDF가 저장되었어요");
        } catch (e) {
            console.error(e);
            toast("PDF 생성에 실패했어요");
        } finally {
            setBtnBusy(btn, false);
        }
    }

    async function saveAsImage(targetId, filename, btn) {
        var el = document.getElementById(targetId);
        if (!el) { toast("결과 영역을 찾을 수 없어요"); return; }
        setBtnBusy(btn, true, "이미지 만드는 중...");
        try {
            var canvas = await captureElement(el);
            var link = document.createElement("a");
            link.download = filename + "_" + todayStr() + ".png";
            link.href = canvas.toDataURL("image/png", 1.0);
            link.click();
            toast("이미지가 저장되었어요");
        } catch (e) {
            console.error(e);
            toast("이미지 저장에 실패했어요");
        } finally {
            setBtnBusy(btn, false);
        }
    }

    function copyShareURL(paramsFn) {
        try {
            var params = typeof paramsFn === "function" ? (paramsFn() || {}) : {};
            var url = new URL(window.location.href);
            // 기존 파라미터 초기화
            Array.from(url.searchParams.keys()).forEach(function (k) { url.searchParams.delete(k); });
            Object.keys(params).forEach(function (k) {
                if (params[k] !== undefined && params[k] !== null && params[k] !== "") {
                    url.searchParams.set(k, String(params[k]));
                }
            });
            var finalURL = url.toString();
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(finalURL).then(
                    function () { toast("링크가 복사되었어요"); },
                    function () { fallbackCopy(finalURL); }
                );
            } else {
                fallbackCopy(finalURL);
            }
        } catch (e) {
            console.error(e);
            toast("링크 복사에 실패했어요");
        }
    }

    function fallbackCopy(text) {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.top = "-9999px";
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand("copy");
            toast("링크가 복사되었어요");
        } catch (e) {
            toast("링크 복사에 실패했어요");
        }
        document.body.removeChild(ta);
    }

    function printPage() {
        window.print();
    }

    var _cfg = null;

    function bind(opts) {
        _cfg = opts || {};
        var root = document.getElementById(opts.actionsId || "resultActions");
        if (!root) return;

        root.addEventListener("click", function (e) {
            var btn = e.target.closest(".ra-btn");
            if (!btn) return;
            var action = btn.dataset.action;
            if (action === "save-pdf") {
                saveAsPDF(_cfg.targetId, _cfg.filename || "결과", btn);
            } else if (action === "save-image") {
                saveAsImage(_cfg.targetId, _cfg.filename || "결과", btn);
            } else if (action === "share-link") {
                copyShareURL(_cfg.shareParams);
            } else if (action === "print") {
                printPage();
            }
        });
    }

    function show(actionsId) {
        var root = document.getElementById(actionsId || (_cfg && _cfg.actionsId) || "resultActions");
        if (root) root.hidden = false;
    }

    function hide(actionsId) {
        var root = document.getElementById(actionsId || (_cfg && _cfg.actionsId) || "resultActions");
        if (root) root.hidden = true;
    }

    window.TrustLayer = {
        bind: bind,
        show: show,
        hide: hide,
        saveAsPDF: saveAsPDF,
        saveAsImage: saveAsImage,
        copyShareURL: copyShareURL,
        print: printPage,
        toast: toast
    };
})(window, document);
