# Rocketpunch Discovery

## URL
- Search URL: https://www.rocketpunch.com/jobs?keyword=qa&seniorities=BEGINNER,JUNIOR
- Title: 채용공고 | IT 스타트업, 유니콘, 외국계, 대기업 채용공고

## Command
- set "PYTHONPATH=src" && .\.venv\Scripts\python src\collectors\rocketpunch_disc.py

## Output
- fixtures/html/rocketpunch-list-20260212-202919.html

## Notes
- Filters intended: 지역=서울, 경력=신입+0~1년, 검색어=QA, 직종=QA/테스터 가능 시
- Observed: 비로그인 상태에서는 검색이 제한됨(“로그인 후 검색 가능” 표시)

## Observations (TODO)
- List item container selector: N/A (login required in saved HTML)
- Title selector: N/A (login required in saved HTML)
- Company selector: N/A (login required in saved HTML)
- Location selector: N/A (login required in saved HTML)
- Experience selector: N/A (login required in saved HTML)
- Posting/closing date selector: N/A (login required in saved HTML)
- Source job id selector/field: N/A (login required in saved HTML)
- Pagination/next page behavior: N/A (login required in saved HTML)

## Evidence
- HTML file path: fixtures/html/rocketpunch-list-20260212-202919.html
- Excerpt (20~60 lines):
<div id="main-content" class="ai_flex-start bg_backgrounds.canvas.standard d_flex flex-sh_0 gap_8px h_100svh p_8px w_100%">
<div class="ai_flex-start as_stretch d_flex flex-d_column trs_all_0.3s_ease max-w_280px">
<div class="ai_flex-start as_stretch d_flex flex-d_column">
<div class="ai_center as_stretch bg_backgrounds.canvas.standard d_flex gap_8px h_tabNav p_8px_4px_8px_8px">
<a style="align-items:center;display:flex" href="/">
<div draggable="false" style="border-radius:0px;cursor:inherit;height:40px;width:40px;padding:0px" class="ai_center d_inline-flex jc_center trs_transform_0.15s_cubic-bezier(0.68,_-0.55,_0.265,_1.55) c_foregrounds.neutral.primary msk_none">
<svg aria-label="icon" color="foregrounds.neutral.primary" fill="currentColor" height="40" role="img" width="40">
<use href="#rocketpunch">
</use>
</svg>
</div>
</a>
<div class="focus:ring_2px_solid focus:ring-c_strokes.surface.brand hover:bg_backgrounds.surface.hover ai_center bg_backgrounds.surface.standard cursor_pointer d_flex flex_1_0_0 gap_8px jc_center max-h_40px max-w_360px min-h_40px p_0px_8px_0_12px bdr_12px">
<div class="ai_center d_flex flex_1_0_0">
<p class="c_foregrounds.neutral.secondary lc_1 ov_hidden tov_ellipsis textStyle_Body.BodyM wb_normal!">로그인 후 검색 가능</p>
</div>
</div>
</div>
</div>
<div class="ai_flex-start as_stretch d_flex flex_1_0_0 flex-d_column gap_16px ov-y_auto py_8px">     
<div class="ai_flex-start as_stretch d_flex flex-d_column">
<div class="ai_flex-start d_flex flex-d_column w_100%">
<div class="w_100%">
<a href="/">
<div class="active:trf_scale(0.98) active:trs_transform_0.1s_cubic-bezier(0.68,_-0.55,_0.265,_1.55) ai_center cursor_pointer d_flex bdr_12px trs_transform_0.15s_cubic-bezier(0.68,_-0.55,_0.265,_1.55) gap_12px p_12px w_100%">
<div draggable="false" style="border-radius:6.4px;cursor:inherit;height:32px;width:32px;padding:6.4px" class="ai_center d_inline-flex jc_center trs_transform_0.15s_cubic-bezier(0.68,_-0.55,_0.265,_1.55) bg_backgrounds.surface.intense c_foregrounds.neutral.tertiary msk_square">
<svg aria-label="icon" color="foregrounds.neutral.tertiary" fill="currentColor" height="19.2" role="img" width="19.2">
<use href="#home-simple-2-solid">
</use>
</svg>
</div>
<div class="d_flex flex_1_0_0 flex-d_column">
<p class="c_foregrounds.neutral.primary textStyle_Body.BodyM_Bold us_none">홈</p>
<p style="display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:1" class="w_100% c_foregegrounds.neutral.secondary ov_hidden tov_ellipsis textStyle_Body.BodyS us_none white-space_pre-line가">가장 빠른 소식</p>
</div>