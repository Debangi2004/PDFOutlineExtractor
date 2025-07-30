
from utils.section_matcher import get_relevance_score

def score_sections(sections, persona):
    # Combine job-to-be-done and focus areas into a single relevance query
    persona_goals = persona.get("job_to_be_done", "") + " " + " ".join(persona.get("focus_areas", []))

    scored = []

    for section in sections:
        section_title = section.get("section_title", "")
        section_text = section.get("refined_text", "")
        
        relevance_score = get_relevance_score(section_title, section_text, persona_goals)

        section["importance_rank"] = relevance_score
        scored.append(section)

    # Sort by semantic relevance
    scored.sort(key=lambda x: x["importance_rank"], reverse=True)
    return scored
