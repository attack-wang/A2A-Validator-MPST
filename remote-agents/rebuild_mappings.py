"""Rebuild mapping tables in op*_data.db to model the chained security scenario.

Chain (all string keys/values):
  IP  --op1--> 威胁组织标签 --op2--> CVE 编号 --op3--> 防御脚本
The output value of one tier is exactly the input key of the next tier, so the
host can feed the value straight through as the next agent's key.
"""
import os
import sqlite3
from contextlib import closing

BASE = os.path.dirname(os.path.abspath(__file__))

# Five representative chains. Group X matches the example in the brief.
GROUPS = [
    # (group tag,                       CVE,                       defense script)
    ("Advanced-Threat-Group-X", "CVE-2026-9999", "Block_Rule_Protocol_v3.sh"),
    ("Advanced-Threat-Group-A", "CVE-2026-9001", "Drop_Payload_Signature_v1.sh"),
    ("Advanced-Threat-Group-B", "CVE-2026-9123", "Isolate_Host_Rule_v2.sh"),
    ("Advanced-Threat-Group-C", "CVE-2026-8888", "Quarantine_File_Rule_v5.sh"),
    ("Advanced-Threat-Group-D", "CVE-2026-9500", "Block_C2_Beacon_v4.sh"),
]

# Several attacker IPs per group -> one group (many-to-one), realistic botnet.
IP_RANGES = {
    "Advanced-Threat-Group-X": ["203.0.113.10", "203.0.113.11", "203.0.113.12",
                                "203.0.113.13", "203.0.113.14"],
    "Advanced-Threat-Group-A": ["198.51.100.20", "198.51.100.21", "198.51.100.22",
                                "198.51.100.23", "198.51.100.24"],
    "Advanced-Threat-Group-B": ["192.0.2.30", "192.0.2.31", "192.0.2.32",
                                "192.0.2.33", "192.0.2.34"],
    "Advanced-Threat-Group-C": ["203.0.113.40", "203.0.113.41", "203.0.113.42",
                                "203.0.113.43", "203.0.113.44"],
    "Advanced-Threat-Group-D": ["198.51.100.50", "198.51.100.51", "198.51.100.52",
                                "198.51.100.53", "198.51.100.54"],
}


def rebuild(db_path, rows):
    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # Recreate the mapping table cleanly as TEXT key/value.
        cur.execute("DROP TABLE IF EXISTS mapping")
        cur.execute("CREATE TABLE mapping (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        cur.executemany("INSERT INTO mapping (key, value) VALUES (?, ?)", rows)
        conn.commit()


def main():
    # op1: IP -> threat group tag
    op1_rows = []
    for tag, _, _ in GROUPS:
        for ip in IP_RANGES[tag]:
            op1_rows.append((ip, tag))
    rebuild(os.path.join(BASE, "op1", "op1_data.db"), op1_rows)

    # op2: threat group tag -> CVE id
    op2_rows = [(tag, cve) for tag, cve, _ in GROUPS]
    rebuild(os.path.join(BASE, "op2", "op2_data.db"), op2_rows)

    # op3: CVE id -> defense script
    op3_rows = [(cve, script) for _, cve, script in GROUPS]
    rebuild(os.path.join(BASE, "op3", "op3_data.db"), op3_rows)

    # Verify the end-to-end chain for every IP.
    print("== Rebuilt mapping tables ==")
    for n, tag, cve, script in [(1,) + g for g in GROUPS]:
        print(f"chain#{n}: {tag:24s} -> {cve:14s} -> {script}")
    print("\n== Sample full traces (first IP per group) ==")
    for tag, cve, script in GROUPS:
        ip = IP_RANGES[tag][0]
        print(f"{ip:15s} -> {tag:24s} -> {cve:14s} -> {script}")

    # sanity cross-db check
    for path, expect in [("op1/op1_data.db", len(op1_rows)),
                         ("op2/op2_data.db", len(op2_rows)),
                         ("op3/op3_data.db", len(op3_rows))]:
        with closing(sqlite3.connect(os.path.join(BASE, path))) as c:
            n = c.execute("SELECT COUNT(*) FROM mapping").fetchone()[0]
            assert n == expect, (path, n, expect)
    print("\nAll rows inserted OK")


if __name__ == "__main__":
    main()
