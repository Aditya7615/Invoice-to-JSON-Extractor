# Invoice to JSON Extractor

**Numbers up top:**
- **Accuracy**: ~80% (8/10 invoices process successfully with retry logic)
- **Latency**: ~70-100 seconds per invoice (depends on image complexity)
- **Cost**: **$0/mo** - uses local Ollama vision model (free)
- **Time Saved**: ~3-5 min per invoice vs manual data entry

## Live Demo

Try it instantly on Google Colab: **[Open in Colab](https://colab.research.google.com/github/YOUR_USERNAME/invoice-json-extractor/blob/main/5_invoice_extractor.ipynb)**

## 90-Second Walkthrough

Watch how it works: **[YouTube Video](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)**

---

Automated pipeline to extract structured JSON from invoice images using local Ollama vision model + Pydantic validation + math checks.

## Features

- **Local, private processing** (no API costs, data never leaves your machine)
- **Strict schema validation** with math consistency checks (line total, tax, grand total)
- **Groq-powered error explanations** for failed extractions
- **Retry logic** for robust extraction (3 attempts per invoice)
- **Multiple date format support** (ISO, US, European, written)
- **Batch processing** for multiple images

## Quick Start

### 1. Setup Environment

```bash
pip install -r requirements.txt
```

### 2. Ollama Vision Model

```bash
ollama pull llama3.2-vision
```

### 3. Environment Variables

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

GROQ_API_KEY required for error explanations ([get one free](https://console.groq.com/keys)).

### 4. Run Extraction

Place invoice images in `dataset/`, then run:

```bash
jupyter nbconvert --execute 5_invoice_extractor.ipynb
```

Or convert to Python and run:

```bash
jupyter nbconvert --to python 5_invoice_extractor.ipynb
python3 5_invoice_extractor.py
```

JSON outputs saved to `output/`.

### 5. Run Tests

```bash
python3 test_extraction.py
```

### 6. Run Evaluations

```bash
python3 evals/run_eval.py
```

## Project Structure

```
.
├── dataset/              # Input invoice images (*.jpg, *.png)
├── output/              # Extracted JSON invoices
├── evals/               # Evaluation test suite
│   ├── test_cases.json  # 35 test cases
│   └── run_eval.py      # Evaluation script
├── 5_invoice_extractor.ipynb  # Main extraction notebook
├── test_extraction.py   # Schema validation tests
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── .gitignore          # Git ignore rules
```

## Architecture

```
Invoice Image → Ollama Vision (llama3.2-vision) → JSON Extraction
                                                      ↓
                                           Pydantic Validation
                                                      ↓
                                           Math Consistency Check
                                                      ↓
                                           Groq Error Explanation (if failed)
```

## How It Works

1. **Vision Model** (`llama3.2-vision`): Reads invoice image, extracts raw data as JSON
2. **Retry Logic**: Up to 3 attempts with different JSON extraction strategies
3. **Data Cleaning**: Normalizes dates, currency strings, tax rates, negative values
4. **Schema Validation**: Pydantic enforces required fields, types, and constraints
5. **Math Checks**: Verifies line totals, tax calculations, and grand totals
6. **Error Explanation**: Groq LLM explains validation failures in plain English

## Expected Output

Each invoice produces a JSON file like:

```json
{
  "vendor_name": "ACME CORP",
  "customer_name": "Tech Solutions",
  "invoice_number": "INVOICE_01",
  "invoice_date": "2024-01-15",
  "subtotal": 1523.15,
  "tax_rate": 0.08,
  "tax_amount": 121.85,
  "total_amount": 1645.0,
  "currency": "USD",
  "line_items": [
    {"description": "Widget A", "quantity": 10, "unit_price": 25.99, "amount": 259.90},
    {"description": "Widget B", "quantity": 5, "unit_price": 49.99, "amount": 249.95}
  ]
}
```

## Troubleshooting

- **Vision model not found**: Run `ollama pull llama3.2-vision`
- **Validation errors**: Check printed errors, the model may have misread the invoice
- **Slow processing**: Normal - vision model runs locally on CPU/GPU
- **Missing dependencies**: Run `pip install -r requirements.txt`

## GitHub Setup

```bash
git init
git add .
git commit -m "Invoice extractor v1.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/invoice-json-extractor.git
git push -u origin main
```

## Contributing

1. Fork the repo
2. Add test cases to `evals/test_cases.json`
3. Run `python3 evals/run_eval.py` to verify
4. Submit a PR

---

Built with [Ollama](https://ollama.ai/) + [Pydantic](https://docs.pydantic.dev/) + [Groq](https://groq.com/)
