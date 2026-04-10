# Invoice to JSON Extractor

**Numbers up top:**
- **Accuracy**: ~80% (8/10 invoices process successfully with retry logic)
- **Latency**: ~70-100 seconds per invoice
- **Cost**: **$0/mo** - uses local Ollama vision model
- **Time Saved**: ~3-5 min per invoice vs manual data entry

---

Automated pipeline to extract structured JSON from invoice images using local Ollama vision model + Pydantic validation + math checks.

## Features

- **Local & Private** - Data never leaves your machine
- **Zero API Costs** - Uses Ollama's free local vision model
- **Strict Validation** - Pydantic schema enforcement
- **Math Consistency** - Verifies line totals, tax, and grand totals
- **Error Explanations** - Groq AI explains validation failures
- **Retry Logic** - 3 attempts per invoice for robustness
- **Multi-format Dates** - ISO, US, European, written formats

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Vision Model

```bash
ollama pull llama3.2-vision
```

### 3. Setup Environment

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env (free at https://console.groq.com/keys)
```

### 4. Run

```bash
jupyter nbconvert --execute invoice_extractor.ipynb
```

JSON outputs appear in `output/`.

## Project Structure

```
Invoice-to-JSON-Extractor/
├── dataset/                    # Place invoice images here (*.jpg, *.png)
├── output/                     # Extracted JSON files
├── evals/
│   ├── test_cases.json         # 33 evaluation test cases
│   └── run_eval.py             # Run: python3 evals/run_eval.py
├── invoice_extractor.ipynb   # Main extraction pipeline
├── test_extraction.py          # Schema validation tests
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── .gitignore                  # Ignores .env, output/, __pycache__/
```

## How It Works

```
Invoice Image
    ↓
Ollama Vision (llama3.2-vision) - Extracts raw JSON
    ↓
Data Cleaning - Dates, currencies, tax rates, negative values
    ↓
Pydantic Validation - Schema enforcement
    ↓
Math Consistency Check - Line totals, tax, grand total
    ↓
Groq Error Explanation - Plain English errors (if failed)
```

## Evaluation Results

```bash
$ python3 evals/run_eval.py

✅ 33/33 tests passing (100%)
- Invoice validation tests: 10
- Date parsing tests: 4
- Math consistency tests: 4
- Validation edge cases: 8
- Schema tests: 2
```

## Example Output

**Input:** Invoice image

**Output:** `output/invoice_01.json`
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

| Issue | Solution |
|-------|----------|
| `Vision model not found` | Run `ollama pull llama3.2-vision` |
| `GROQ_API_KEY not set` | Add key to `.env` file |
| Slow processing | Normal - vision model runs locally |
| Validation errors | Check output errors - model may have misread invoice |

## Tech Stack

- [Ollama](https://ollama.ai/) - Local vision model
- [Pydantic](https://docs.pydantic.dev/) - Schema validation
- [Groq](https://groq.com/) - Error explanations

---

Star ⭐ if this helped!
