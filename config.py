import os
import sqlite3
import shutil
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, "revenue_recovery.db")

def ensure_db_initialized(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Check if events table exists and has rows
        try:
            cur.execute("SELECT COUNT(*) FROM events")
            cnt = cur.fetchone()[0]
            if cnt > 0:
                conn.close()
                return
        except Exception:
            pass

        # Create schema
        schema_path = os.path.join(BASE_DIR, "db", "schema.sql")
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()

        # Seed initial rich recovery events
        seed_events = [
            (
                "evt_pay_01", "payment_failed", "Acme Corp (Stripe)", "stripe",
                '{"amount": 6100, "reason": "soft_decline_mandate", "currency": "USD"}', "resolved",
                "insufficient_funds", 0.94, "Card mandate soft decline diagnosed; retried successfully after balance refresh.",
                "retry_payment", '{"delay_hours": 24, "max_retries": 3}', 0,
                "act_01", "retry_payment", "success", "Mandate retry sequenced successfully: $6,100 recovered."
            ),
            (
                "evt_chk_01", "checkout_abandoned", "Globex Retail (Shopify)", "shopify_checkout",
                '{"amount": 28400, "items": 14, "customer_phone": "+1-555-0199"}', "resolved",
                "price_sensitive", 0.91, "Customer dropped off at final checkout screen.",
                "send_update_link", '{"discount_code": "RECOVER10", "channel": "hinglish_voice"}', 0,
                "act_02", "send_update_link", "success", "Hinglish voice recovery executed; cart completed ($28,400 saved)."
            ),
            (
                "evt_sub_01", "subscription_failed", "TechFlow SaaS", "chargebee",
                '{"amount": 4200, "plan": "enterprise_monthly", "cycle": 12}', "resolved",
                "expired_card", 0.96, "Corporate credit card expired at billing cycle renewal.",
                "send_update_link", '{"grace_period_days": 7}', 0,
                "act_03", "send_update_link", "success", "Account payment update link clicked & verified ($4,200 retained)."
            ),
            (
                "evt_rec_01", "invoice_overdue", "Wayne Logistics", "oracle_netsuite",
                '{"amount": 2450, "invoice_num": "INV-2026-904", "days_overdue": 45}', "escalated",
                "customer_dispute", 0.89, "B2B Net-30 overdue terms exceeded. PO reconciliation mismatch reported.",
                "escalate_human", '{"reason": "High-value invoice > $500 with dispute flag"}', 1,
                "act_04", "escalate_human", "pending", "Escalated to Lead Recovery Specialist for promise-to-pay confirmation."
            )
        ]

        for item in seed_events:
            (
                eid, etype, cust, src, raw, status,
                d_reason, d_conf, d_expl,
                dec_action, dec_params, dec_hum,
                act_id, act_action, act_res, act_det
            ) = item

            cur.execute(
                "INSERT OR IGNORE INTO events (id, type, customer_id, source, raw_payload, status) VALUES (?, ?, ?, ?, ?, ?)",
                (eid, etype, cust, src, raw, status)
            )
            cur.execute(
                "INSERT OR IGNORE INTO diagnoses (event_id, reason_category, confidence, explanation) VALUES (?, ?, ?, ?)",
                (eid, d_reason, d_conf, d_expl)
            )
            cur.execute(
                "INSERT OR IGNORE INTO decisions (event_id, action, params, requires_human) VALUES (?, ?, ?, ?)",
                (eid, dec_action, dec_params, dec_hum)
            )
            cur.execute(
                "INSERT OR IGNORE INTO actions_log (id, event_id, action, result, detail) VALUES (?, ?, ?, ?, ?)",
                (act_id, eid, act_action, act_res, act_det)
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Init DB note: {e}")

def get_db_path():
    if os.environ.get("VERCEL"):
        db_file = "/tmp/revenue_recovery.db"
        if not os.path.exists(db_file):
            if os.path.exists(DEFAULT_DB):
                try:
                    shutil.copyfile(DEFAULT_DB, db_file)
                except Exception:
                    pass
            ensure_db_initialized(db_file)
        return db_file
    
    # Local environment
    if not os.path.exists(DEFAULT_DB):
        ensure_db_initialized(DEFAULT_DB)
    return DEFAULT_DB

def get_connection():
    db_path = get_db_path()
    return sqlite3.connect(db_path)