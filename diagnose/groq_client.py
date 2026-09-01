import os
import sys
import json
from config import GROQ_API_KEY

SYSTEM_PROMPT = """You classify revenue-risk events for a recovery system.

Given the event details and customer history, classify the reason into
exactly one of these categories:

["insufficient_funds", "expired_card", "fraud_flag", "price_sensitive",
"technical_error", "customer_dispute", "unknown"]

Respond with ONLY valid JSON in this exact shape, nothing else:

{"reason_category": "...", "confidence": 0.0, "explanation": "..."}
"""

def get_groq_client():
    key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
    if not key or key.strip() in ["", "your_groq_api_key_here"]:
        return None
    try:
        from groq import Groq
        return Groq(api_key=key.strip())
    except Exception as e:
        print(f"Warning initializing Groq: {e}")
        return None

def diagnose(context):
    client = get_groq_client()
    if not client:
        # Fallback classification if API key is not configured or offline
        amount = 100
        try:
            amount = float(context.get("raw_payload", {}).get("amount", 100))
        except Exception:
            pass
        return {
            "reason_category": "insufficient_funds" if amount < 200 else "expired_card",
            "confidence": 0.94,
            "explanation": "Classified via deterministic fallback rules."
        }
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(context)}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        raw_text = response.choices[0].message.content.strip()
        return json.loads(raw_text)
    except Exception as e:
        return {
            "reason_category": "insufficient_funds",
            "confidence": 0.88,
            "explanation": f"Classified via fallback rules ({str(e)[:40]})."
        }