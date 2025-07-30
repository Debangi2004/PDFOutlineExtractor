import os
import json
import argparse
from datetime import datetime

from persona_loader import load_persona
from utils.pdf_reader import extract_pdf_sections
from utils.scorer import score_sections
from utils.json_writer import write_output_json
from utils.section_matcher import is_relevant_section

import time

start_time = time.time()

def get_all_pdfs(input_dir):
    return [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".pdf")]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona", type=str, required=True, help="Path to persona JSON file")
    parser.add_argument("--input", type=str, default="input", help="Directory containing PDF files")
    parser.add_argument("--output", type=str, default="output/challenge1b_output.json", help="Output JSON path")
    args = parser.parse_args()

    # Step 1: Load Persona
    persona = load_persona(args.persona)

    # Step 2: Load Documents
    pdf_files = get_all_pdfs(args.input)
    if not pdf_files:
        print("❌ No PDF files found in input folder.")
        exit(1)
    print(f"📄 Found {len(pdf_files)} PDF files.")

    # Step 3: Extract all sections
    all_sections = []
    for file_path in pdf_files:
        extracted = extract_pdf_sections(file_path)
        all_sections.extend(extracted)

    # Step 4: Score & Rank
    ranked_sections = score_sections(all_sections, persona)

    # Step 5: Create Output
    write_output_json(ranked_sections, pdf_files, persona, args.output)

    end_time = time.time()
    elapsed = end_time - start_time
    if elapsed > 60:
        print(f"⏱️ Time limit exceeded: {elapsed:.2f}s")
        exit(1)
    else:
        print(f"✅ Done in {elapsed:.2f}s! Output written to: {args.output}")

if __name__ == "__main__":
    main()
