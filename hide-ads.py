#!/usr/bin/env python3
"""
광고 일시 숨김 스크립트
- 카카오 애드핏, 쿠팡 파트너스 배너를 HTML 주석으로 감싸서 비활성화
- 코드를 삭제하지 않고 주석 처리만 함
- 이미 주석 처리된 것은 건너뜀
"""

import os
import re
import glob

BASE_DIR = "/Users/hyuntaeshin/Desktop/JoCoding/folder_1"
EXCLUDE_DIRS = {"design-concepts", "blog-posts"}


def get_html_files():
    """대상 HTML 파일 목록 반환 (제외 폴더 필터링)"""
    all_html = glob.glob(os.path.join(BASE_DIR, "**", "*.html"), recursive=True)
    filtered = []
    for f in all_html:
        rel = os.path.relpath(f, BASE_DIR)
        parts = rel.split(os.sep)
        if parts[0] not in EXCLUDE_DIRS:
            filtered.append(f)
    return sorted(filtered)


def is_inside_adsense_hide_comment(lines, target_line_idx):
    """
    target_line_idx 줄이 <!-- ADSENSE-HIDE: ... --> 주석 블록 안에 있는지 확인.
    ADSENSE-HIDE 주석은 중첩된 HTML 주석을 포함할 수 있으므로,
    '<!-- ADSENSE-HIDE:' 로 시작하는 줄과 그에 대응하는 단독 '-->' 줄을 찾아서 판단.
    """
    # 위로 올라가면서 <!-- ADSENSE-HIDE: 를 찾기
    for i in range(target_line_idx, -1, -1):
        stripped = lines[i].strip()
        if stripped.startswith('<!-- ADSENSE-HIDE:'):
            # 이 블록의 닫는 --> 찾기 (단독 줄 또는 줄 끝이 -->)
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '-->':
                    if j >= target_line_idx:
                        return True  # target이 이 주석 블록 안에 있음
                    else:
                        break  # 이 주석 블록은 target 전에 닫혔음
            break
    return False


def find_div_block(lines, div_start_line):
    """div_start_line부터 시작하여 중첩 div를 고려해 닫는 </div> 라인을 찾기"""
    depth = 0
    for i in range(div_start_line, len(lines)):
        line = lines[i]
        depth += len(re.findall(r'<div[\s>]', line))
        depth -= len(re.findall(r'</div>', line))
        if depth <= 0:
            return i
    return None


def hide_kakao_adfit(content, filename):
    """카카오 애드핏 광고 div를 주석으로 감싸기"""
    changes = []
    lines = content.split('\n')

    # kakao_ad_area가 포함된 줄 번호 찾기
    kakao_lines = []
    for i, line in enumerate(lines):
        if 'kakao_ad_area' in line:
            kakao_lines.append(i)

    if not kakao_lines:
        return content, changes

    # 각 kakao_ad_area에 대해 감싸는 div 블록 찾기
    blocks_to_hide = []  # (start_line, end_line) 튜플

    for kakao_line in kakao_lines:
        # 이미 ADSENSE-HIDE 주석 안에 있는지 확인
        if is_inside_adsense_hide_comment(lines, kakao_line):
            continue

        # 위로 올라가면서 감싸는 div 시작 찾기
        div_start_line = None
        for i in range(kakao_line, -1, -1):
            stripped = lines[i].strip()
            if stripped.startswith('<div'):
                div_start_line = i
                break

        if div_start_line is None:
            continue

        # div 끝 찾기
        div_end_line = find_div_block(lines, div_start_line)
        if div_end_line is None:
            continue

        # 바로 위에 <!-- 카카오 애드핏 --> 주석이 있으면 포함
        start_line = div_start_line
        if div_start_line > 0 and '카카오 애드핏' in lines[div_start_line - 1]:
            start_line = div_start_line - 1

        blocks_to_hide.append((start_line, div_end_line))

    if not blocks_to_hide:
        return content, changes

    # 뒤에서부터 처리 (줄 번호 변경 방지)
    for start_line, end_line in reversed(blocks_to_hide):
        block_lines = lines[start_line:end_line + 1]
        block_text = '\n'.join(block_lines)

        # 들여쓰기 감지
        first_line = block_lines[0]
        indent = len(first_line) - len(first_line.lstrip())
        indent_str = first_line[:indent]

        comment_start = f"{indent_str}<!-- ADSENSE-HIDE: 카카오 애드핏"
        comment_end = f"{indent_str}-->"

        new_lines = [comment_start] + block_lines + [comment_end]
        lines[start_line:end_line + 1] = new_lines

        changes.append(f"  [카카오 애드핏] 라인 ~{start_line + 1} 주석 처리")

    return '\n'.join(lines), changes


def hide_coupang_banner(content, filename):
    """쿠팡 파트너스 배너 div를 주석으로 감싸기"""
    changes = []
    lines = content.split('\n')

    # coupang-banner div가 있는 줄 찾기
    coupang_lines = []
    for i, line in enumerate(lines):
        if '<div class="coupang-banner">' in line:
            coupang_lines.append(i)

    if not coupang_lines:
        return content, changes

    blocks_to_hide = []

    for div_start_line in coupang_lines:
        # 이미 ADSENSE-HIDE 주석 안에 있는지 확인
        if is_inside_adsense_hide_comment(lines, div_start_line):
            continue

        # div 끝 찾기
        div_end_line = find_div_block(lines, div_start_line)
        if div_end_line is None:
            continue

        # 바로 위에 <!-- 쿠팡 파트너스 배너 --> 주석이 있으면 포함
        start_line = div_start_line
        if div_start_line > 0 and '쿠팡 파트너스' in lines[div_start_line - 1]:
            start_line = div_start_line - 1

        blocks_to_hide.append((start_line, div_end_line))

    if not blocks_to_hide:
        return content, changes

    # 뒤에서부터 처리
    for start_line, end_line in reversed(blocks_to_hide):
        block_lines = lines[start_line:end_line + 1]

        first_line = block_lines[0]
        indent = len(first_line) - len(first_line.lstrip())
        indent_str = first_line[:indent]

        comment_start = f"{indent_str}<!-- ADSENSE-HIDE: 쿠팡 파트너스"
        comment_end = f"{indent_str}-->"

        new_lines = [comment_start] + block_lines + [comment_end]
        lines[start_line:end_line + 1] = new_lines

        changes.append(f"  [쿠팡 파트너스] 라인 ~{start_line + 1} 주석 처리")

    return '\n'.join(lines), changes


def main():
    html_files = get_html_files()
    print(f"대상 HTML 파일: {len(html_files)}개")
    print(f"제외 폴더: {', '.join(EXCLUDE_DIRS)}")
    print("=" * 60)

    total_modified = 0
    total_kakao = 0
    total_coupang = 0

    for filepath in html_files:
        rel_path = os.path.relpath(filepath, BASE_DIR)
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()

        content = original
        all_changes = []

        # 카카오 애드핏 처리
        content, kakao_changes = hide_kakao_adfit(content, rel_path)
        all_changes.extend(kakao_changes)

        # 쿠팡 파트너스 처리
        content, coupang_changes = hide_coupang_banner(content, rel_path)
        all_changes.extend(coupang_changes)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_modified += 1
            total_kakao += len(kakao_changes)
            total_coupang += len(coupang_changes)
            print(f"\n[수정됨] {rel_path}")
            for change in all_changes:
                print(change)
        else:
            print(f"[변경없음] {rel_path}")

    print("\n" + "=" * 60)
    print(f"처리 완료!")
    print(f"  수정된 파일: {total_modified}개")
    print(f"  카카오 애드핏 주석 처리: {total_kakao}건")
    print(f"  쿠팡 파트너스 주석 처리: {total_coupang}건")


if __name__ == "__main__":
    main()
