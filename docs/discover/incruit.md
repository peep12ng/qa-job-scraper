# Incruit Discovery

## URL
- Search URL: [(fill)](https://search.incruit.com/list/search.asp?col=job&kw=qa&memty=2000)
- Title: (fill)

## Command
- set "PYTHONPATH=src" && .\.venv\Scripts\python src\collectors\incruit_disc.py

## Output
- fixtures/html/incruit-list-YYYYMMDD-HHMMSS.html

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
- HTML file path: C:\Users\xyz\workspace\qa-job-scraper\fixtures\html\incruit-list-20260212-201652.html
- Excerpt (20~60 lines):
<ul class="c_row" jobno="2512150002766">
				<li class="c_col ">
					<div class="cell_first">
						<!-- <input type="checkbox" name="JobPostChecked" id="JobList_2512150002766" value="2512150002766" class="c_cChk_ipt" /><label for="JobList_2512150002766" class="c_cChk"><span></span></label> -->
						<div class="cl_top">
						
							<a href="https://www.incruit.com/company/22605393" class="cpname" target="_blank">베이글코드</a>
							
							<button class="btns_wish wish_corp_icon wish_heart" f_mem="08E9C0495D0902B917A6E642451A0AF8AF33C28AC367D5AB115C28EB6CE2AE37" f_comp="1CB2A46B8C67A5598CB51AFF0BC0F719A3E75A289EE89B1F000908299C33E5F7" f_act="CI" title="관심기업">관심기업</button>
						
						</div>
						<div class="cl_btm">
							 <a href="https://job.incruit.com/jobdb_list/searchjob.asp?ct=9&amp;ty=1&amp;cd=4" target="_blank"><span class="sm-txt-icon icon">벤처기업</span></a>
						</div>
					</div>
					<div class="cell_mid">
						<div class="cl_top">
							<a href="https://job.incruit.com/jobdb_info/jobpost.asp?job=2512150002766&amp;src=etc*search" target="_blank">[CVS] <span class="highlight">QA</span></a>
							<button type="button" id="scrap_icon_v2_nor_2512150002766" onclick="goCL(this,'19091','job','2512150002766_스크랩');JobPostScrapAdd('IncJob', '', '', '2512150002766', 'nor');" jobno="2512150002766" class="scrap_icon_v2_2512150002766 dev_ScrapBt btns_scraps " title="클릭하면 스크랩됩니다">스크랩</button>
						</div>
						<div class="cl_md">
							
							<span>서울 강남구</span>
							
							<span>신입/경력(3년↑)</span>
							
							<span>학력무관</span>
							
							<span>정규직</span>
							
						</div>
						<div class="cl_btm">
							<span>게임(Game),</span> <span>고객상담·관리·수퍼바이저,</span> <span>컨텐츠·사이트운영</span>
						</div>
					</div>
					<div class="cell_last">
						<div class="cl_btm"><span>상시</span><span>(2025.12.15 등록)</span></div>
						<div class="cl_top">
							<button onclick="goCL(this,'19033',G_SECONDARY_DOMAIN,'목록_홈페이지지원_2512150002766');window.open(G_HOSTNAME_JOB+'/jobdb_info/jobpost.asp?job=2512150002766');" class="btns_homepage_submit" bl_job="2512150002766">홈페이지 지원</button>
						</div>
					</div>
				</li>
			</ul>
