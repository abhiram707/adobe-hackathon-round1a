# Adobe Hackathon Round 1A - Enhanced PDF Outline Extractor

## 📌 Overview
This Dockerized solution extracts structured outlines (Title, H1-H3 headings with page numbers) from PDFs and outputs a clean JSON format.

## 🧠 Approach
- Uses PyMuPDF for parsing
- KMeans clustering on font size for heading levels
- Heuristics to filter out non-heading text and extract title

## 🏗️ Folder Structure
```
pdf_outline_extractor/
├── app/
│   ├── input/         # Put your PDFs here
│   ├── output/        # JSON output will be saved here
│   └── extract_outline.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 Run the Project
```bash
docker build --platform linux/amd64 -t pdfoutliner .
docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output --network none pdfoutliner
```