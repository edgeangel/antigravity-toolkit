#!/usr/bin/env python3
"""Validation structurelle d'un skill Antigravity.

Usage:
    python3 validate_skill.py <chemin-du-skill>

Vérifie :
  - SKILL.md présent
  - Frontmatter YAML valide avec name et description
  - Description < 500 caractères
  - evals/evals.json bien formé (si présent)

Retourne un JSON avec les résultats de chaque check.
Aucune dépendance externe (stdlib Python uniquement).
"""

import json
import os
import re
import sys


def validate_skill(skill_path: str) -> dict:
    """Valide la structure d'un skill et retourne un rapport JSON."""
    checks = []
    skill_path = os.path.expanduser(skill_path)

    # Check 1: SKILL.md exists
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    skill_md_exists = os.path.isfile(skill_md_path)
    checks.append({
        "name": "skill_md_exists",
        "passed": skill_md_exists,
        "message": "SKILL.md present" if skill_md_exists else "SKILL.md not found"
    })

    if not skill_md_exists:
        return _build_report(skill_path, checks)

    # Read SKILL.md content
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check 2: Valid YAML frontmatter
    frontmatter = _extract_frontmatter(content)
    has_frontmatter = frontmatter is not None
    checks.append({
        "name": "valid_frontmatter",
        "passed": has_frontmatter,
        "message": "Valid YAML frontmatter" if has_frontmatter else "Missing or invalid YAML frontmatter"
    })

    if not has_frontmatter:
        return _build_report(skill_path, checks)

    # Check 3: name field present
    has_name = bool(frontmatter.get("name"))
    checks.append({
        "name": "has_name",
        "passed": has_name,
        "message": f"name: {frontmatter.get('name')}" if has_name else "Missing 'name' in frontmatter"
    })

    # Check 4: description field present and not empty
    description = frontmatter.get("description", "")
    has_description = bool(description and str(description).strip())
    checks.append({
        "name": "has_description",
        "passed": has_description,
        "message": "description present" if has_description else "Missing or empty 'description' in frontmatter"
    })

    # Check 5: description length < 500 chars
    desc_len = len(str(description).strip()) if description else 0
    desc_ok = desc_len < 500
    checks.append({
        "name": "description_length",
        "passed": desc_ok,
        "message": f"description length: {desc_len} chars" + ("" if desc_ok else " (> 500 chars)")
    })

    # Check 6: SKILL.md line count < 500
    line_count = len(content.splitlines())
    lines_ok = line_count < 500
    checks.append({
        "name": "skill_md_length",
        "passed": lines_ok,
        "message": f"SKILL.md: {line_count} lines" + ("" if lines_ok else " (> 500 lines, consider references/)")
    })

    # Check 7: ea- prefix convention (for EA skills)
    name = frontmatter.get("name", "")
    is_ea = name.startswith("ea-") if name else False
    checks.append({
        "name": "ea_prefix",
        "passed": is_ea,
        "message": f"EA prefix: {'yes' if is_ea else 'no (not an EA skill or missing prefix)'}"
    })

    # Check 8: evals/evals.json (if present)
    evals_path = os.path.join(skill_path, "evals", "evals.json")
    if os.path.isfile(evals_path):
        try:
            with open(evals_path, "r", encoding="utf-8") as f:
                evals_data = json.load(f)
            has_skill_name = bool(evals_data.get("skill_name"))
            has_evals = isinstance(evals_data.get("evals"), list) and len(evals_data["evals"]) > 0
            evals_valid = has_skill_name and has_evals
            checks.append({
                "name": "evals_json_valid",
                "passed": evals_valid,
                "message": f"evals.json: {len(evals_data.get('evals', []))} evals" if evals_valid else "evals.json: invalid structure"
            })
            if has_evals:
                for eval_item in evals_data["evals"]:
                    missing = [field for field in ["id", "prompt", "assertions"] if field not in eval_item]
                    if missing:
                        checks.append({
                            "name": f"eval_{eval_item.get('id', '?')}_fields",
                            "passed": False,
                            "message": f"Eval {eval_item.get('id', '?')}: missing fields {missing}"
                        })
        except json.JSONDecodeError as e:
            checks.append({
                "name": "evals_json_valid",
                "passed": False,
                "message": f"evals.json: invalid JSON - {e}"
            })
    else:
        checks.append({
            "name": "evals_json_present",
            "passed": True,
            "message": "evals.json: not present (optional)"
        })

    return _build_report(skill_path, checks)


def _extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content using regex (no yaml dependency)."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    raw = match.group(1)
    result = {}
    current_key = None
    current_value_lines = []

    for line in raw.split("\n"):
        # Simple key: value
        kv_match = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if kv_match:
            # Save previous key
            if current_key:
                result[current_key] = _join_value(current_value_lines)
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip()
            if value == ">" or value == "|":
                current_value_lines = []
            else:
                current_value_lines = [value.strip('"').strip("'")]
        elif current_key and line.startswith("  "):
            # Continuation line for multiline values
            current_value_lines.append(line.strip())
        elif current_key and line.strip() == "":
            current_value_lines.append("")

    # Save last key
    if current_key:
        result[current_key] = _join_value(current_value_lines)

    return result if result else None


def _join_value(lines: list) -> str:
    """Join multiline value lines."""
    return " ".join(l for l in lines if l).strip()


def _build_report(skill_path: str, checks: list) -> dict:
    """Build the validation report."""
    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    return {
        "skill_path": skill_path,
        "checks": checks,
        "passed": passed,
        "failed": failed,
        "total": len(checks),
        "status": "PASS" if failed == 0 else "FAIL"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_skill.py <skill-path>")
        sys.exit(1)
    result = validate_skill(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASS" else 1)
