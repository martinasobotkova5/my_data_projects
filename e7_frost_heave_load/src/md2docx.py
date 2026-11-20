"""md (GFM, s HTML seznamy v tabulkách) → docx přes pandoc; okraje tabulek, tučné záhlaví, šířky sloupců.
Použití: python3 src/md2docx.py dodavatele_E7.md E7_dodavatele.docx"""
import sys, subprocess, tempfile, os, docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
src, out = sys.argv[1], sys.argv[2]
with tempfile.TemporaryDirectory() as tmp:
    h = os.path.join(tmp, "x.html")
    subprocess.run(["pandoc", "-f", "gfm", "-t", "html", src, "-o", h], check=True)
    subprocess.run(["pandoc", "-f", "html", "-t", "docx", h, "-o", out], check=True)
d = docx.Document(out)
for t in d.tables:
    pr = t._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        x = OxmlElement(f"w:{e}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "4"); x.set(qn("w:color"), "999999"); b.append(x)
    pr.append(b)
    for c in t.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs: r.bold = True
d.save(out)

# šířky sloupců podle obsahu, menší písmo a menší odsazení odrážek v tabulkách
from docx.shared import Cm, Pt
d = docx.Document(out)
sec = d.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7); sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = sec.bottom_margin = Cm(2)
W = 17.0
for t in d.tables:
    n = len(t.columns)
    L = [max(4, sum(len(r.cells[i].text) for r in t.rows) / len(t.rows)) for i in range(n)]
    w = [x ** 0.7 for x in L]; s = sum(w); w = [max(1.2, W * x / s) for x in w]
    k = W / sum(w); w = [x * k for x in w]
    t.autofit = False
    grid = t._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))): gc.set(qn("w:w"), str(int(w[i] * 567)))
    for r in t.rows:
        for i, c in enumerate(r.cells):
            c.width = Cm(w[i])
            for p in c.paragraphs:
                for run in p.runs: run.font.size = Pt(9)
                pPr = p._p.pPr
                if pPr is not None and pPr.numPr is not None:
                    p.paragraph_format.left_indent = Cm(0.45); p.paragraph_format.first_line_indent = Cm(-0.35)
d.save(out)
