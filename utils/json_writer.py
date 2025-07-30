import json
from datetime import datetime
import os

def write_output_json(sections, documents, persona, output_path):
    output = {
        "metadata": {
            "input_documents": [doc.split('/')[-1] for doc in documents],
            "persona": persona.get("persona", ""),
            "job_to_be_done": persona.get("job_to_be_done", ""),
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    # ✅ Limit to top 10 relevant sections
    top_sections = sorted(sections, key=lambda x: x["importance_rank"], reverse=True)[:10]

    if not top_sections:
        print("Warning: No relevant sections found to write in output.")

    for sec in top_sections:
        output["extracted_sections"].append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "section_title": sec["section_title"],
            "importance_rank": sec["importance_rank"]
        })

        output["sub_section_analysis"].append({
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page_number"]
        })

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
