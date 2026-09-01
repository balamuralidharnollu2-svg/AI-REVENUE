CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL,
    converted_to_event INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    source TEXT,
    raw_payload TEXT,
    status TEXT DEFAULT 'new',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnoses (
    event_id TEXT PRIMARY KEY REFERENCES events(id),
    reason_category TEXT,
    confidence REAL,
    explanation TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
    event_id TEXT PRIMARY KEY REFERENCES events(id),
    action TEXT,
    params TEXT,
    requires_human INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actions_log (
    id TEXT PRIMARY KEY,
    event_id TEXT REFERENCES events(id),
    action TEXT,
    result TEXT,
    detail TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);