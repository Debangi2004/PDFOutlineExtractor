
from sentence_transformers import SentenceTransformer, util

# Load the model (once, globally)
model = SentenceTransformer('models/all-MiniLM-L6-v2')  # Offline model path

def get_relevance_score(section_title, section_text, persona_goals):
    """
    Returns similarity score between a section and persona goals (higher = more relevant).
    """
    section_input = section_title + " " + section_text
    section_embedding = model.encode(section_input, convert_to_tensor=True)
    persona_embedding = model.encode(persona_goals, convert_to_tensor=True)
    
    score = util.pytorch_cos_sim(section_embedding, persona_embedding)
    return score.item()
    
