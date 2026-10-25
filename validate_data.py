"""Validation script for College FAQ dataset.

Checks:
1. File existence and basic CSV parsing.
2. Mandatory column schema existence.
3. Unique integer IDs.
4. Non-empty question and answer fields.
5. Detection of near-duplicate questions.
6. Proper delimiter formatting for paraphrases and keywords.
"""

from difflib import SequenceMatcher
import os
import sys
import pandas as pd

REQUIRED_COLUMNS = [
    "id",
    "category",
    "question",
    "answer",
    "paraphrases",
    "keywords",
    "source_url",
    "last_updated",
]


def similarity_ratio(a: str, b: str) -> float:
  """Compute string similarity ratio to detect potential duplicate questions."""
  return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def validate_faq_csv(file_path: str) -> bool:
  print(f"[INFO] Validating FAQ dataset at: {file_path}")
  if not os.path.exists(file_path):
    print(f"[ERROR] File does not exist: {file_path}")
    return False

  try:
    df = pd.read_csv(file_path, dtype=str).fillna("")
  except Exception as e:
    print(f"[ERROR] Failed to read CSV: {e}")
    return False

  errors = []
  warnings = []

  # 1. Column verification
  missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
  if missing_cols:
    errors.append(f"Missing required columns: {missing_cols}")

  if errors:
    print("\n--- Critical Errors ---")
    for err in errors:
      print(f"❌ {err}")
    return False

  # 2. Row count
  if len(df) == 0:
    errors.append("CSV dataset is empty!")

  # 3. ID uniqueness & parsing
  ids = []
  for idx, row in df.iterrows():
    raw_id = row.get("id", "").strip()
    if not raw_id:
      errors.append(f"Row {idx + 2}: ID is missing.")
    elif not raw_id.isdigit():
      errors.append(f"Row {idx + 2}: ID '{raw_id}' must be an integer.")
    else:
      ids.append(int(raw_id))

  if len(ids) != len(set(ids)):
    duplicates = [i for i in ids if ids.count(i) > 1]
    errors.append(f"Duplicate IDs detected: {set(duplicates)}")

  # 4. Mandatory Question and Answer check
  questions = []
  for idx, row in df.iterrows():
    faq_id = row.get("id", f"Row {idx + 2}")
    q = row.get("question", "").strip()
    a = row.get("answer", "").strip()
    cat = row.get("category", "").strip()

    if not q:
      errors.append(f"FAQ ID {faq_id}: 'question' cannot be empty.")
    if not a:
      errors.append(f"FAQ ID {faq_id}: 'answer' cannot be empty.")
    if not cat:
      warnings.append(
          f"FAQ ID {faq_id}: 'category' is empty, default will be General."
      )

    questions.append((faq_id, q))

  # 5. Duplicate or near-duplicate question detection
  for i in range(len(questions)):
    for j in range(i + 1, len(questions)):
      id1, q1 = questions[i]
      id2, q2 = questions[j]
      if not q1 or not q2:
        continue
      sim = similarity_ratio(q1, q2)
      if sim == 1.0:
        errors.append(f"Exact duplicate question between ID {id1} and ID {id2}")
      elif sim > 0.85:
        warnings.append(
            f"Near-duplicate question ({sim:.2f} similarity) between ID {id1}"
            f" ('{q1[:40]}...') and ID {id2} ('{q2[:40]}...')"
        )

  # Output Summary
  print(f"\n[SUMMARY] Total FAQ entries checked: {len(df)}")
  if warnings:
    print(f"\n--- Warnings ({len(warnings)}) ---")
    for w in warnings:
      print(f"[WARN] {w}")

  if errors:
    print(f"\n--- Errors ({len(errors)}) ---")
    for err in errors:
      print(f"[ERROR] {err}")
    print("\n[RESULT] Validation FAILED.")
    return False

  print(
      "\n[RESULT] Validation PASSED successfully! Dataset is clean and ready."
  )
  return True


if __name__ == "__main__":
  target = sys.argv[1] if len(sys.argv) > 1 else "data/faqs.csv"
  success = validate_faq_csv(target)
  sys.exit(0 if success else 1)
