import json
import os
from pathlib import Path
from datetime import date
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, List

# Schema from notebook
class LineItem(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    amount: float = Field(..., ge=0)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v, info):
        if 'quantity' in info.data and 'unit_price' in info.data:
            expected = round(info.data['quantity'] * info.data['unit_price'], 2)
            if abs(v - expected) > 0.01:
                raise ValueError(f'Amount {v} != qty * price ({expected})')
        return v

class Invoice(BaseModel):
    vendor_name: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1)
    invoice_number: str = Field(..., min_length=1)
    invoice_date: date
    subtotal: float = Field(..., ge=0)
    tax_rate: float = Field(..., ge=0, le=1)
    tax_amount: float = Field(..., ge=0)
    total_amount: float = Field(..., ge=0)
    line_items: List[LineItem] = Field(..., min_length=1)
    currency: str = Field(default="USD")
    due_date: Optional[date] = None
    shipping_amount: Optional[float] = Field(None, ge=0)
    discount_amount: Optional[float] = Field(None, ge=0)
    vendor_address: Optional[str] = None
    vendor_phone: Optional[str] = None
    vendor_email: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    customer_address: Optional[str] = None
    customer_email: Optional[str] = None
    payment_terms: Optional[str] = None
    payment_method: Optional[str] = None
    bank_details: Optional[str] = None
    notes: Optional[str] = None

OUTPUT_DIR = 'output'

def test_all_json_files():
    json_files = list(Path(OUTPUT_DIR).glob('*.json'))
    print(f"Found {len(json_files)} JSON files")
    assert len(json_files) > 0, "No JSON files found"
    
    failed = []
    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            invoice = Invoice.model_validate(data)
            print(f"✅ {json_file.name}: Valid (Total: {invoice.total_amount} {invoice.currency})")
        except Exception as e:
            print(f"❌ {json_file.name}: Failed validation - {str(e)}")
            failed.append(json_file.name)
    
    assert not failed, f"Failed files: {failed}"

if __name__ == '__main__':
    test_all_json_files()
    print("All tests passed!")
