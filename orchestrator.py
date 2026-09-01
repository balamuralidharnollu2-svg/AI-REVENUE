import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect.invoice_scanner import scan_invoices
from diagnose.run_diagnosis import run_diagnosis
from decide.run_decision import run_decision
from execute.run_execution import run_execution


def run_pipeline():
    print("=== Running full recovery pipeline ===\n")

    print("Step 1: Detect")
    scan_invoices()

    print("\nStep 2: Diagnose")
    run_diagnosis()

    print("\nStep 3: Decide")
    run_decision()

    print("\nStep 4: Execute")
    run_execution()

    print("\n=== Pipeline complete ===")


if __name__ == "__main__":
    run_pipeline()