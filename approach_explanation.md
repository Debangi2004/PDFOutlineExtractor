# Structured Document Intelligence - Approach

Our solution for the Adobe Hackathon focuses on building a lightweight, CPU-only pipeline that extracts structured document outlines from a collection of PDFs, with an emphasis on relevance to specific personas.

## Problem Understanding

The goal is to process 3–5 PDFs within 60 seconds, extract key hierarchical sections (Title, H1, H2, H3), and map them to a given persona's needs. The challenge required a solution that works offline, uses no internet access, and keeps model size under 1GB.

## Methodology

### 1. PDF Parsing and Heading Extraction

We used PyMuPDF (`fitz`) to read each PDF and analyze text blocks. Unlike simple text parsing, our approach leverages font size to infer heading structure. Font size hierarchy is dynamically calculated for each document. The largest font is assumed to be the Title, followed by H1, H2, and H3.

This method is rule-based, lightweight, and fast — ideal for CPU environments with strict runtime constraints.

### 2. Persona Matching

Each persona is defined via a JSON file containing their goals, focus areas, and relevant keywords. We use cosine similarity between TF-IDF vectors to match extracted sections against the persona description, ranking and filtering based on relevance.

This avoids heavy deep learning models, keeping the model size minimal and offline-compatible.

## Dockerized Execution

The solution is containerized using Docker, with pre-installed dependencies and pre-downloaded models (if any). No network access is needed during execution.

### Execution Instructions

## 1. Overview

This system provides semantic PDF extraction using MiniLM for finding relevant sections based on job-to-be-done queries. The solution is optimized for CPU-only operation with ≤1GB model size and ≤60 second processing time.

## 2. Prerequisites

- Docker installed
- At least 2GB RAM available
- Collection folders with input files (Collection1, Collection2, Collection3)

## 3. Quick Start

### 1. Build the Docker Image

```bash
docker build -t adobe_hackathon . 
```

### 2. Run the Processor

```bash
# Run the Processor
docker run adobe_hackathon
# Process all collections
docker run --rm -v $(pwd):/app adobe_hackathon
```

### 3. Check Results

Output files will be generated in each collection folder:
- `Collection1/challenge1b_output.json`
- `Collection2/challenge1b_output.json`
- `Collection3/challenge1b_output.json`

## Detailed Usage

### Command Line Options

```bash
# Process all collections
python collection_processor.py

# Process specific collection
python collection_processor.py --collection Collection1

# Process with custom model
python collection_processor.py --model all-MiniLM-L12-v2

# Process with verbose output
python collection_processor.py --verbose
```

### Input Format

Each collection should contain:
- `challenge1b_input.json` - Challenge configuration
- `input/` folder with PDF documents

Example input structure:
```
Collection1/
├── challenge1b_input.json
└── input/
    ├── doc1.pdf
    ├── doc2.pdf
    ├── doc3.pdf
    └── doc4.pdf
```

### Output Format

The system generates structured JSON output with:

1. **Metadata**
   - Input documents list
   - Persona information
   - Job to be done
   - Processing timestamp

2. **Extracted Sections**
   - Document source
   - Page number
   - Section title
   - Importance rank (semantic relevance score)

3. **Sub-section Analysis**
   - Document details
   - Refined text content
   - Page number constraints
   - Relevance scores

## Performance Monitoring

### Processing Time
- **Target**: ≤60 seconds for 3-5 documents
- **Typical**: 10-30 seconds
- **Monitoring**: Check console output for timing information

### Memory Usage
- **Model Size**: ~80MB (MiniLM-L6-v2)
- **Runtime Memory**: 200-500MB
- **Total Usage**: <1GB

### CPU Usage
- **Optimization**: CPU-only operation
- **Threading**: Single-threaded for consistency
- **Efficiency**: Optimized for CPU inference

## Troubleshooting

### Common Issues

1. **Model Download Issues**
   ```bash
   # Pre-download model
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

2. **Memory Issues**
   - Ensure at least 2GB RAM available
   - Close other applications
   - Use smaller model if needed: `all-MiniLM-L6-v2`

3. **PDF Processing Errors**
   - Check PDF file integrity
   - Ensure PDFs contain extractable text
   - Verify file permissions

4. **Timeout Issues**
   - Monitor processing time in console
   - Check system resources
   - Consider processing fewer documents at once

### Debug Mode

```bash
# Run with debug output
python collection_processor.py --debug

# Check model information
python -c "from utils.semantic_extractor import SemanticPDFExtractor; e = SemanticPDFExtractor(); print(e.get_model_info())"
```

## Advanced Configuration

### Model Selection

```python
# Use different model variants
extractor = SemanticPDFExtractor('all-MiniLM-L6-v2')   # Fast, 384 dims
extractor = SemanticPDFExtractor('all-MiniLM-L12-v2')  # Accurate, 768 dims
```

### Custom Processing

```python
from utils.semantic_extractor import SemanticPDFExtractor

# Initialize extractor
extractor = SemanticPDFExtractor()

# Process single PDF
sections = extractor.find_top_sections('document.pdf', 'your query', top_k=3)

# Process multiple PDFs
sections = extractor.find_top_sections_multiple_pdfs(['doc1.pdf', 'doc2.pdf'], 'your query', top_k=3)
```

## Validation

### Output Validation

1. **Check JSON Structure**
   ```bash
   python -c "import json; data = json.load(open('Collection1/challenge1b_output.json')); print('Valid JSON structure')"
   ```

2. **Verify Required Fields**
   - Metadata section present
   - Extracted sections with relevance scores
   - Sub-section analysis included

3. **Performance Validation**
   - Processing time < 60 seconds
   - Memory usage < 1GB
   - CPU-only operation confirmed

## Integration

### With Existing System

The semantic extractor integrates with the existing persona-based system:

```python
from utils.enhanced_scorer import EnhancedSemanticScorer
from persona_loader import load_persona

# Load persona
persona = load_persona('persona.json')

# Use enhanced scorer
scorer = EnhancedSemanticScorer()
ranked_sections = scorer.score_sections(sections, persona)
```

### Custom Workflows

```python
from collection_processor import CollectionProcessor

# Process specific collection
processor = CollectionProcessor()
output = processor.process_collection('Collection1')
processor.save_output('Collection1', output)
```

## Support

For issues or questions:
1. Check console output for error messages
2. Verify input file formats
3. Ensure system requirements are met
4. Review performance metrics in output

The system is designed to be robust and self-contained, providing reliable semantic PDF extraction within the specified constraints. 