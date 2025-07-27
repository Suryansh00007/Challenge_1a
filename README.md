# 📄 PDF Outline Extractor (Challenge 1A)

This solution extracts a structured **outline** from PDF documents, identifying:
- The document **title**
- Headings at levels **H1**, **H2**, and **H3** (based on font sizes)
- Their **page numbers**

It generates a **schema-compliant JSON output** for each PDF, and is designed to run **offline** within memory and time constraints.

---

## 🚀 What It Does

- Reads PDF files (up to 50 pages) from the `/app/input` directory
- For each PDF:
  - Extracts `title` from metadata or filename
  - Detects heading-like text and classifies them as `H1`, `H2`, or `H3` based on font size
  - Captures their page number
  - Outputs results to `/app/output/filename.json`
- Supports multilingual headings (e.g., English, Hindi, Japanese, Arabic)
- Validates each output against a predefined JSON schema (`output_schema.json`)

---

## 🧰 Key Libraries Used

| Library      | Purpose |
|--------------|---------|
| **PyMuPDF (`fitz`)** | To parse PDFs, extract text blocks, font sizes, and layout |
| **unicodedata** | To check for heading-like content across multiple languages |
| **jsonschema** | To validate the final JSON output structure |

---

## 📥 Example Output

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
