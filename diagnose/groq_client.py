import os
import sys

# Allow running this file directly from the subdirectory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from groq import Groq
from config import GROQ_API_KEY


# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


# System prompt for the diagnosis agent
SYSTEM_PROMPT = """You classify revenue-risk events for a recovery system.

Given the event details and customer history, classify the reason into
exactly one of these categories:

["insufficient_funds", "expired_card", "fraud_flag", "price_sensitive",
"technical_error", "customer_dispute", "unknown"]

Respond with ONLY valid JSON in this exact shape, nothing else:

{"reason_category": "...", "confidence": 0.0, "explanation": "..."}
"""


def diagnose(context):
    """
    Diagnose a revenue-risk event using the Groq LLM.

    Args:
        context (dict): Event details and customer history.

    Returns:
        dict: Diagnosis result.
    """

    response = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(context),
            },
        ],
    )

    # Get model response
    raw_text = response.choices[0].message.content.strip()

    # Remove Markdown code fences if the model adds them
    raw_text = (
        raw_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Convert response from JSON string to Python dictionary
    try:
        result = json.loads(raw_text)

    except json.JSONDecodeError:
        result = {
            "reason_category": "unknown",
            "confidence": 0.0,
            "explanation": f"Could not parse model response: {raw_text}",
        }

    return result


# Test the diagnosis agent when this file is run directly
if __name__ == "__main__":

    test_context = {
        "event": {
            "type": "payment_failed",
            "amount": 49.99,
            "failure_code": "insufficient_funds",
        },
        "customer": {
            "payment_failures": 2,
            "previous_successful_payments": 10,
        },
    }

    print("Testing Groq diagnosis agent...")
    print()

    result = diagnose(test_context)

    print("Diagnosis result:")
    print(json.dumps(result, indent=2))