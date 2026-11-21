from pathlib import Path
from PIL import Image, ImageDraw
import fitz

out = Path(__file__).resolve().parents[1] / "tests" / "samples"
out.mkdir(parents=True, exist_ok=True)
(out / "clean.txt").write_text("This is a normal sample.", encoding="utf-8")
(out / "marked.txt").write_text("Example marker: WALLED_SENSITIVE", encoding="utf-8")

for name, content in [
    ("clean.pdf", "This is a clean PDF sample."),
    ("marked.pdf", "This PDF contains WALLED_SENSITIVE."),
]:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), content, fontsize=14)
    doc.save(out / name)
    doc.close()

for name, content in [
    ("clean.png", "CLEAN SAMPLE"),
    ("marked.png", "WALLED_SENSITIVE"),
]:
    image = Image.new("RGB", (800, 220), "white")
    draw = ImageDraw.Draw(image)
    draw.text((30, 80), content, fill="black")
    image.save(out / name)

print(f"Samples created in {out}")
