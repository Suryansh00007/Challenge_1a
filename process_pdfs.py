import os
import json
import unicodedata
from pathlib import Path
import fitz  # PyMuPDF
from jsonschema import validate, ValidationError

# Debug: show PyMuPDF version
print(fitz.__doc__)

def is_heading(txt):
    """
    Likely heading if 3+ chars and has a letter
    """
    if len(txt) < 3:
        return False
    return any(unicodedata.category(c).startswith("L") for c in txt)

def get_outline(pdf):
    doc = fitz.open(pdf)
    title = doc.metadata.get("title") or pdf.stem
    heads = []
    f_map = {}

    for i in range(len(doc)):
        pg = doc[i]
        blocks = pg.get_text("dict")["blocks"]

        for blk in blocks:
            for ln in blk.get("lines", []):
                for span in ln.get("spans", []):
                    txt = span["text"].strip()
                    if not is_heading(txt):
                        continue
                    sz = round(span["size"])
                    f_map.setdefault(sz, []).append((txt, i + 1))  # 1-based page

    sz_sorted = sorted(f_map.keys(), reverse=True)
    lvls = ["H1", "H2", "H3"]
    sz_lvl = {sz: lvls[idx] for idx, sz in enumerate(sz_sorted[:3])}

    seen = set()
    for sz in sz_sorted:
        lvl = sz_lvl.get(sz)
        if not lvl:
            continue
        for txt, pg in f_map[sz]:
            clean = " ".join(txt.split())
            k = (clean.lower(), pg)
            if k in seen:
                continue
            seen.add(k)
            heads.append({
                "level": lvl,
                "text": clean,
                "page": pg
            })

    return {
        "title": title.strip(),
        "outline": heads
    }

def main():
    in_dir = Path("sample_dataset/pdfs")
    out_dir = Path("sample_dataset/outputs")
    sch_path = Path("sample_dataset/schema/output_schema.json")

    with open(sch_path, "r", encoding="utf-8") as f:
        sch = json.load(f)

    for pdf in in_dir.glob("*.pdf"):
        print(f"📄 Processing: {pdf.name}")
        try:
            res = get_outline(pdf)
            validate(instance=res, schema=sch)
            out_file = out_dir / f"{pdf.stem}.json"
            with open(out_file, "w", encoding="utf-8") as f_out:
                json.dump(res, f_out, indent=2, ensure_ascii=False)
            print(f"✅ Saved: {out_file.name}")
        except ValidationError as ve:
            print(f" Validation failed for {pdf.name}: {ve.message}")
        except Exception as ex:
            print(f" Error processing {pdf.name}: {ex}")

if __name__ == "__main__":
    main()
