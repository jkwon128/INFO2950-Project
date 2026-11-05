from pathlib import Path
import nbformat
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
nb=nbformat.read(root/'Phase3_Report.ipynb',as_version=4)
exporter=HTMLExporter(template_name='basic')
body,_=exporter.from_notebook_node(nb)
css='''
@page { size: Letter; margin: 0.58in 0.62in 0.58in; }
* { box-sizing: border-box; }
body { font: 10pt/1.36 Arial, Helvetica, sans-serif; color: #202b33; margin:0; }
h1,h2,h3 {color:#203f53; line-height:1.2; break-after:avoid;}
h1 {font-size:25pt; margin:0 0 14px;} h2{font-size:16pt;margin:14px 0 12px;}
h3{font-size:12pt;margin:14px 0 8px;} p{margin:8px 0 10px;orphans:3;widows:3;}
a{color:#215d7d;text-decoration:none;} strong{font-weight:700;}
.page-break{break-before:page; height:0;}
.cell{margin:0 0 9px; padding:0;} .prompt{display:none;}
.input{background:#f3f5f7;border-left:3px solid #b9cbd5;padding:9px 11px; margin:10px 0;break-inside:avoid;}
.input pre{font:8pt/1.3 'Menlo','Courier New',monospace;margin:0;white-space:pre-wrap;overflow-wrap:anywhere;}
.output pre{font:8.5pt/1.38 'Menlo','Courier New',monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:9px 0;}
.output_png{break-inside:avoid;text-align:center;} .output_png img{max-width:100%;height:auto;max-height:4.4in;object-fit:contain;}
.output_area{break-inside:avoid;} .output_wrapper{margin:6px 0 12px;}
table{border-collapse:collapse;width:100%;font-size:9pt;line-height:1.32;margin:10px 0 14px;break-inside:avoid;}
th,td{padding:5px 6px;border-bottom:1px solid #dce2e6;text-align:left!important;vertical-align:top;}
th{background:#eaf0f4;color:#203f53;font-weight:600;} tbody tr:nth-child(even){background:#f7f9fa;}
code{font-family:'Menlo','Courier New',monospace;font-size:8.6pt;overflow-wrap:anywhere;}
ul,ol{padding-left:21px;} li{margin:6px 0;}
.anchor-link{display:none;} .output_stderr{color:#9c3425;}
@media screen{body{max-width:850px;padding:40px;margin:auto;} .page-break{margin-top:45px;border-top:1px solid #ddd;}}
'''
html='<!doctype html><html><head><meta charset="utf-8"><title>INFO 2950 Phase 3</title><style>'+css+'</style></head><body>'+body+'</body></html>'
path=root/'Phase3_Report.html';path.write_text(html)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    page=browser.new_page()
    page.goto(path.as_uri(),wait_until='networkidle')
    page.emulate_media(media='print')
    page.pdf(path=str(root/'Phase3_Report.pdf'),format='Letter',print_background=True,
        display_header_footer=True,header_template='<div></div>',
        footer_template='<div style="font-family:Arial;font-size:8px;color:#61717d;width:100%;padding:0 45px;display:flex;justify-content:space-between"><span>INFO 2950 | Phase 3 | Inflation and monthly S&amp;P 500 returns</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
        prefer_css_page_size=True)
    browser.close()
print('Exported HTML and PDF from the fully executed notebook.')
