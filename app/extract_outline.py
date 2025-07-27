
import os
import json
import fitz  
from collections import defaultdict, Counter
from sklearn.cluster import KMeans
import numpy as np
import re
import logging

logging.basicConfig(level=logging.INFO)

def is_heading_candidate(span):
    text = span['text'].strip()
    if not text or len(text) < 3:
        return False
    if re.match(r"^\d+$", text):  
        return False
    if re.match(r"^table of contents", text, re.I):
        return False
    return True

def extract_candidates(doc):
    spans = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if is_heading_candidate(span):
                        spans.append({
                            "text": span['text'].strip(),
                            "font": span['font'],
                            "size": round(span['size'], 2),
                            "flags": span['flags'],  
                            "page": page_num + 1,
                            "y": span['bbox'][1]
                        })
    return spans

def assign_heading_levels(spans):
    size_counter = Counter([span["size"] for span in spans])
    common_sizes = [size for size, _ in size_counter.most_common(6)]
    if len(common_sizes) < 3:
        return {}
    size_arr = np.array(common_sizes).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, n_init=10).fit(size_arr)
    cluster_centers = sorted([c[0] for c in kmeans.cluster_centers_], reverse=True)
    size_to_level = {}
    for size in common_sizes:
        cluster_id = kmeans.predict([[size]])[0]
        rank = cluster_centers.index(sorted(cluster_centers, reverse=True)[cluster_id])
        size_to_level[size] = f"H{rank + 1}"
    return size_to_level

def get_title(spans):
    first_page = [s for s in spans if s['page'] == 1]
    if not first_page:
        return "Untitled Document"
    largest = sorted(first_page, key=lambda s: (-s['size'], abs(s['y'] - 100)))[0]
    return largest['text']

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    spans = extract_candidates(doc)
    size_to_level = assign_heading_levels(spans)
    outline = []

    for span in spans:
        level = size_to_level.get(span['size'])
        if level:
            outline.append({
                "level": level,
                "text": span["text"],
                "page": span["page"]
            })
    title = get_title(spans)
    return {"title": title, "outline": outline}

def main(input_dir="/app/input", output_dir="/app/output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            try:
                logging.info(f"Processing {file}")
                result = extract_outline(input_path)
                with open(output_path, "w") as out:
                    json.dump(result, out, indent=2)
            except Exception as e:
                logging.error(f"Failed to process {file}: {e}")

if __name__ == "__main__":
    main()
