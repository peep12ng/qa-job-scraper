# JobKorea Discovery

## URL
- Search URL: https://www.jobkorea.co.kr/Search/?Page_No=1&duty=1000247&careerType=1%2C2&careerMax=1&stext=qa
- Title: qa

## Command
- set "PYTHONPATH=src" && .\.venv\Scripts\python src\collectors\jobkorea_disc.py

## Output
- fixtures/html/jobkorea-list-YYYYMMDD-HHMMSS.html

## Notes
- Filters intended: 지역=서울, 경력=신입+0~1년, 키워드=QA, 직종=QA/테스터(가능 시)

## Observations (TODO)
- List item container selector:
- Title selector:
- Company selector:
- Location selector:
- Experience selector:
- Posting/closing date selector:
- Source job id selector/field:
- Pagination/next page behavior:

## Evidence
- HTML file path: C:\Users\xyz\workspace\qa-job-scraper\fixtures\html\jobkorea-list-20260212-135739.html
- Excerpt (20~60 lines):
<div class="Box_bgColor_white__1wwr54u0 Box_borderColor_default__1wwr54u5 Box_borderSize_1__1wwr54ud styles_p_space0__dk46ts61 styles_radius_radius16__dk46ts9d Shadow_root_list__bm2zcc6 dlua7o0" data-sentry-component="CardJob" data-sentry-element="Box" data-sentry-source-file="index.tsx" style="width:100%;cursor:pointer">
              <div class="Flex_display_flex__i0l0hl2 Flex_direction_column__i0l0hl4" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
               <div class="Flex_display_flex__i0l0hl2 Flex_gap_space20__i0l0hl11 styles_p_space28__dk46ts8d dlua7o2" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                <a data-interactive="true" data-sentry-component="CompanyLogo" data-sentry-element="BaseLink" data-sentry-source-file="index.tsx" href="https://www.jobkorea.co.kr/Recruit/GI_Read/48356639?Oem_Code=C1&amp;logpath=1&amp;stext=qa&amp;listno=18&amp;sc=630" rel="noopener noreferrer" style="width:76px;height:76px" target="_blank">
                 <div class="Box_bgColor_white__1wwr54u0 Box_borderColor_gray200__1wwr54u6 Box_borderSize_1__1wwr54ud styles_px_space6__dk46ts4i styles_radius_radius8__dk46ts9g Flex_display_flex__i0l0hl2 Flex_align_center__i0l0hl8 Flex_justify_center__i0l0hld styles_flex-shrink_0__dk46tsa9 styles_overflow_hidden__dk46ts9s styles_position_relative__dk46tsa5" data-sentry-element="Box" data-sentry-source-file="index.tsx" style="height:76px;width:76px;border-radius:99px">
                  <img alt="㈜미리디 로고" data-nimg="1" data-sentry-component="Image" data-sentry-element="NextImage" data-sentry-source-file="index.tsx" decoding="async" height="0" loading="lazy" src="https://imgs.jobkorea.co.kr//Images/Logo/128/m/i/2290u00uwlopdzn_2620d7bdadada2ud.gif?p=y&amp;hash=c" style="color:transparent;width:auto;height:auto;max-width:100%;max-height:100%" width="0"/>
                 </div>
                </a>
                <div class="" data-sentry-element="Block" data-sentry-source-file="index.tsx" style="width:100%">
                 <div class="Flex_display_flex__i0l0hl2 Flex_align_center__i0l0hl8 Flex_justify_space-between__i0l0hlf styles_position_relative__dk46tsa5 styles_mb_space6__dk46ts4f" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                  <div class="Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_align_center__i0l0hl8" data-sentry-component="BadgeItem" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                   <span class="Typography_variant_size13__344nw28 Typography_weight_medium__344nw2d Typography_color_theme-secondary2__344nw2h" data-accent-color="theme-secondary2" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                    유연근무제 시행중
                   </span>
                  </div>
                  <div class="styles_position_absolute__dk46tsa6" style="right:0;top:0">
                   <button data-interactive="true" data-sentry-component="BaseButton" data-sentry-source-file="index.tsx" type="button">
                    <i class="jds-icon jds-icon--system_scrap Icon_root__1516qwb0 Icon_color_gray300__1516qwbb Icon_size_28__1516qwbn">
                    </i>
                    <span style="position:absolute;border:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;word-wrap:normal">
                     스크랩
                    </span>
                   </button>
                  </div>
                 </div>
                 <div class="styles_mb_space2__dk46ts4t" data-sentry-element="Block" data-sentry-source-file="index.tsx">
                  <a class="Flex_display_flex__i0l0hl2 Flex_gap_space6__i0l0hl1g Flex_align_center__i0l0hl8 styles_mb_space2__dk46ts4t" data-interactive="true" data-sentry-element="BaseLink" data-sentry-source-file="index.tsx" href="https://www.jobkorea.co.kr/Recruit/GI_Read/48356639?Oem_Code=C1&amp;logpath=1&amp;stext=qa&amp;listno=18&amp;sc=630" rel="noopener noreferrer" style="max-width:700px" target="_blank">
                   <span class="Typography_variant_size18__344nw25 Typography_weight_medium__344nw2d Typography_color_gray900__344nw2m Typography_truncate__344nw2y" data-accent-color="gray900" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                    [커머스 플랫폼] Jr. QA 엔지니어
                   </span>
                  </a>
                 </div>
                 <a class="Flex_display_inline-flex__i0l0hl1 Flex_gap_space6__i0l0hl1g Flex_align_center__i0l0hl8 styles_mb_space20__dk46ts2h" data-interactive="true" data-sentry-element="BaseLink" data-sentry-source-file="index.tsx" href="https://www.jobkorea.co.kr/Recruit/GI_Read/48356639?Oem_Code=C1&amp;logpath=1&amp;stext=qa&amp;listno=18&amp;sc=630" rel="noopener noreferrer" target="_blank">
                  <span class="Typography_variant_size16__344nw26 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o Typography_truncate__344nw2y" data-accent-color="gray700" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                   ㈜미리디
                  </span>
                  <span class="Typography_variant_size11__344nw2a Typography_weight_regular__344nw2e Typography_color_gray500__344nw2p styles_flex-shrink_0__dk46tsa9" data-accent-color="gray500" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                  </span>
                 </a>
                 <div class="Flex_display_flex__i0l0hl2 Flex_gap_space10__i0l0hlm Flex_direction_column__i0l0hl4" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                  <div class="Flex_display_flex__i0l0hl2 Flex_justify_space-between__i0l0hlf" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                   <div class="Flex_display_flex__i0l0hl2 Flex_gap_space8__i0l0hlv" data-sentry-element="Flex" data-sentry-source-file="index.tsx" style="max-width:643px">
                    <div class="Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_align_center__i0l0hl8 styles_flex-shrink_0__dk46tsa9 styles_px_space10__dk46tsm _10fvqwx0" data-sentry-component="GrayChip" data-sentry-element="Flex" data-sentry-source-file="index.tsx" style="height:30px;min-width:auto">
                     <div class="styles_flex-shrink_0__dk46tsa9" data-sentry-element="Block" data-sentry-source-file="index.tsx" style="width:16px">
                      <div class="emoji--basicemoji-place2" style="width:16px;height:16px;background-size:16px;background-position:center;background-repeat:no-repeat">
                      </div>
                     </div>
                     <span class="Typography_variant_size14__344nw27 Typography_weight_regular__344nw2e Typography_color_gray900__344nw2m Typography_truncate__344nw2y" data-accent-color="gray900" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                      서울 구로구
                     </span>
                    </div>
                    <div class="Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_align_center__i0l0hl8 styles_flex-shrink_1__dk46tsaa styles_px_space10__dk46tsm _10fvqwx0" data-sentry-component="GrayChip" data-sentry-element="Flex" data-sentry-source-file="index.tsx" style="height:30px;min-width:0">
                     <div class="styles_flex-shrink_0__dk46tsa9" data-sentry-element="Block" data-sentry-source-file="index.tsx" style="width:16px">
                      <div class="emoji--basicemoji-briefcase" style="width:16px;height:16px;background-size:16px;background-position:center;background-repeat:no-repeat">
                      </div>
                     </div>
                     <span class="Typography_variant_size14__344nw27 Typography_weight_regular__344nw2e Typography_color_gray900__344nw2m Typography_truncate__344nw2y" data-accent-color="gray900" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                      솔루션·SI·CRM·ERP, 웹개발자, QA
                     </span>
                    </div>
                   </div>
                   <div class="" data-interactive="true">
                    <button class="Flex_display_flex__i0l0hl2 Flex_align_center__i0l0hl8 Flex_justify_center__i0l0hld styles_flex-shrink_0__dk46tsa9 styles_px_space10__dk46tsm _16czznu2 _16czznu0" data-sentry-component="BaseButton" data-sentry-element="BaseButton" data-sentry-source-file="index.tsx" style="height:32px;width:90px" type="button">
                     <span class="Typography_variant_size12__344nw29 Typography_weight_medium__344nw2d Typography_color_gray900__344nw2m" data-accent-color="gray900" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                      홈페이지 지원
                     </span>
                    </button>
                   </div>
                  </div>
                  <div class="Flex_display_flex__i0l0hl2 Flex_align_center__i0l0hl8 Flex_justify_space-between__i0l0hlf" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                   <div class="Flex_display_flex__i0l0hl2 Flex_gap_space2__i0l0hl1j Flex_align_center__i0l0hl8" data-sentry-element="Flex" data-sentry-source-file="index.tsx" style="max-width:565px">
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o styles_flex-shrink_0__dk46tsa9" data-accent-color="gray700" data-sentry-element="Typography" data-sentry-source-file="index.tsx">
                     경력1년↑
                    </span>
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o Typography_truncate__344nw2y" data-accent-color="gray700">
                     •
                    </span>
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o Typography_truncate__344nw2y" data-accent-color="gray700">
                     유연근무
                     <!-- -->
                     ,
                     <!-- -->
                     사내 동호회 지원
                     <!-- -->
                     ,
                     <!-- -->
                     저녁 식사 지원
                     <!-- -->
                     ,
                     <!-- -->
                     리프레시 휴가
                    </span>
                   </div>
                   <div class="Flex_display_flex__i0l0hl2 Flex_gap_space2__i0l0hl1j styles_flex-shrink_0__dk46tsa9" data-sentry-element="Flex" data-sentry-source-file="index.tsx">
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o" data-accent-color="gray700">
                     01/07(수) 등록
                    </span>
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o" data-accent-color="gray700">
                     •
                    </span>
                    <span class="Typography_variant_size13__344nw28 Typography_weight_regular__344nw2e Typography_color_gray700__344nw2o" data-accent-color="gray700">
                     03/06(금) 마감
                    </span>
                   </div>
                  </div>
                 </div>
                </div>
               </div>
              </div>
             </div>
