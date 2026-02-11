# Saramin Discovery

## URL
- Search URL:https://www.saramin.co.kr/zf_user/search?searchType=search&searchword=qa&loc_mcd=101000&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&exp_cd=1%2C2&exp_min=1&exp_max=1&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y title=qa

## Command
- set "PYTHONPATH=src" && .\.venv\Scripts\python src\collectors\saramin_disc.py

## Output
- fixtures/html/saramin-list-20260211-211049.html

## Notes
- Filters applied: 지역=서울, 경력=신입+0~1년, 키워드=QA, 직종=QA/테스터(가능 시)

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
- HTML file path: fixtures/html/saramin-list-20260211-211049.html
- Excerpt (20~60 lines):
<div class="area_job">
                                    <h2 class="job_tit">
                <a target="_blank" title="QA 경력직" onclick="try{s_trackApply(this, 'search', 'generic')}catch(e){};" rel="" class="data_layer" data-data_layer="keyword_free|paid_n" href="/zf_user/jobs/relay/view?view_type=search&amp;rec_idx=52896496&amp;location=ts&amp;searchword=qa&amp;searchType=search&amp;paid_fl=n&amp;search_uuid=f51db613-dc9d-49c5-b1db-79a77897a7df"><span><b>QA</b> 경력직</span></a>             </h2>
                            <div class="toolTipWrap wrap_scrap">
                                        <a style="cursor:pointer" class="icon_scrap_star" onclick="Saramin.btnJob('scrap',this,'','list');" scraped="n" rec_idx="52896496" data-pattern="{&quot;t_category&quot;:&quot;search&quot;,&quot;t_content&quot;:&quot;generic&quot;,&quot;t_scnid&quot;:&quot;&quot;,&quot;search_uuid&quot;:&quot;f51db613-dc9d-49c5-b1db-79a77897a7df&quot;,&quot;t_ref&quot;:&quot;search&quot;}" title="스크랩" onmouseover="Saramin.favorTooltip(this, 'on');" onmouseout="Saramin.favorTooltip(this, 'off');">
                        <img src="//www.saraminimage.co.kr/common/bul_sri_star.png" alt="스크랩">
                    </a>
                    <div class="toolTip sri_tooltip_scrap">
                        <span class="tail tail_bottom_center"></span>
                        <div class="toolTipCont txtCenter">스크랩</div>
                    </div>
                </div>
                        <div class="job_date">
                <span class="date">~ 02/20(금)</span>
                <button class="sri_btn_xs" title="클릭하면 입사지원할 수 있는 창이 뜹니다." onclick="try{quickApplyForm('52896496','','t_category=search&amp;t_content=generic&amp;t_scnid=&amp;search_uuid=f51db613-dc9d-49c5-b1db-79a77897a7df&amp;t_ref=search', 'searchType=search&amp;searchword=qa'); return false;} catch (e) {}; return false;" onmousedown="try{n_trackEvent('apply','list','quick_apply');}catch(e){}"><span class="sri_btn_immediately">입사지원</span></button>            </div>
            <div class="job_condition">
                <span><a target="_blank" href="/zf_user/area-recruit/area-list/area/101000/areamode/mcode">서울</a>  <a target="_blank" href="/zf_user/area-recruit/area-list/area/101010">강남구</a></span> <span>경력 1~4년</span> <span>고졸↑</span> <span>정규직</span>             </div>
                            <div class="job_sector">
                    <b><a target="_blank" href="/zf_user/jobs/list/job-category?cat_kewd=99">QA/테스터</a></b>, <b><a target="_blank" href="/zf_user/jobs/list/job-category?cat_kewd=89">유지보수</a></b>, <a target="_blank" href="/zf_user/jobs/list/job-category?cat_kewd=100">SE(시스템엔지니어)</a>, <a target="_blank" href="/zf_user/jobs/list/job-category?cat_kewd=142">API</a>, <a target="_blank" href="/zf_user/jobs/list/industry?ind_key=30118">소프트웨어개발</a>                    <span class="job_day">수정일 26/01/22</span>                                    </div>
                    </div>
                            <div class="area_corp">
                <strong class="corp_name">
                                            <a href="/zf_user/company-info/view?csn=Um9CRGlTOVNNM3JzY2lUaU01cjVTZz09" target="_blank" class="track_event data_layer" data-track_event="total_search|search_recruit|com_info_btn" data-data_layer="recruit_com|com_name">
                            (유)알렌의서재                        </a>
                        
                </strong>
                <div class="toolTipWrap wrap_interested_corp"><button type="button" csn="Um9CRGlTOVNNM3JzY2lUaU01cjVTZz09" title="관심기업 등록" del_fl="n" aria-pressed="false" class="interested_corp" onclick="try{Saramin.btnJob('favor', this, '', 'list');}catch(e){}" onmouseover="Saramin.favorTooltip(this, 'on');" onmouseout="Saramin.favorTooltip(this, 'off');" first_nudge="off"><span>관심기업 등록</span></button><div class="toolTip"><span class="tail tail_bottom_center"></span><div class="toolTipCont txtCenter">관심기업 등록</div></div></div>                    <div class="area_btn" value="Um9CRGlTOVNNM3JzY2lUaU01cjVTZz09">
                                                    <div class="area_corp_info">
                                <a href="/zf_user/company-info/view?csn=Um9CRGlTOVNNM3JzY2lUaU01cjVTZz09" target="_blank" class="btn_info track_event data_layer company_popup" data-track_event="total_search|search_recruit|com_info_btn" data-data_layer="recruit_com|com_info">
                                    기업정보
                                </a>
                                <div class="lpop_corp_info area_preview">
                                </div>
                            </div>
                                                                                                    <button type="button" class="btn_recruit track_event" data-csn_encrypt="Um9CRGlTOVNNM3JzY2lUaU01cjVTZz09" data-track_event="total_search|search_recruit|com_recruit_collect_btn">
                                공고 모아보기 +
                            </button>
                                            </div>
                            </div>
                <div class="similar_recruit"></div>
    </div>
        <div class="item_recruit" value="52983618" data-data_layer="keyword_free|paid_n_quick">
                    <div class="area_badge">
            <span class="badge ">
                <svg>
                    <use xlink:href="#rec_title_tag_emoji_invest"></use>
                </svg>
                스타트업            </span>
            </div>