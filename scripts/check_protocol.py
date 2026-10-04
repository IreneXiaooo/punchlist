"""Validate draft contracts without executing any task commands."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def local_references(document: dict) -> None:
    """Resolve every local JSON pointer, including unused definitions."""
    def visit(value):
        if isinstance(value, dict):
            if "$ref" in value:
                reference = value["$ref"]
                if not reference.startswith("#/"):
                    raise ValueError(f"Non-local reference is not supported: {reference}")
                target = document
                for token in reference[2:].split("/"):
                    target = target[token.replace("~1", "/").replace("~0", "~")]
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)


def semantic_errors(plan: dict) -> list[str]:
    """Additional invariants not represented by the 0.2 JSON Schema."""
    errors = []
    steps = plan["steps"]
    by_id = {step["id"]: step for step in steps}
    if len(by_id) != len(steps):
        errors.append("Step IDs must be unique")

    for step in steps:
        sid = step["id"]
        dependencies = step.get("depends_on", [])
        if len(set(dependencies)) != len(dependencies):
            errors.append(f"{sid}: duplicate dependencies")
        for dependency in dependencies:
            if dependency not in by_id:
                errors.append(f"{sid}: unknown dependency {dependency}")
        if len(set(step["lanes"])) != len(step["lanes"]):
            errors.append(f"{sid}: duplicate lanes")
        checks = step["acceptance"]
        if len({check["id"] for check in checks}) != len(checks):
            errors.append(f"{sid}: duplicate acceptance check IDs")
        for check in checks:
            if check.get("kind") == "review" and check["reviewer_lane"] == "script":
                errors.append(f"{sid}: script cannot be an independent model reviewer")

    visiting, visited = set(), set()

    def visit(sid):
        if sid in visiting:
            raise ValueError("Dependency graph contains a cycle")
        if sid in visited or sid not in by_id:
            return
        visiting.add(sid)
        for dependency in by_id[sid].get("depends_on", []):
            visit(dependency)
        visiting.remove(sid)
        visited.add(sid)

    try:
        for sid in by_id:
            visit(sid)
    except ValueError as error:
        errors.append(str(error))

    for limit in plan.get("budget", {}).get("limits", []):
        if limit.get("reserve", 0) > limit["max"]:
            errors.append("Budget reserve exceeds total limit")
        if limit["unit"] == "quota_fraction" and limit["max"] > 1:
            errors.append("A single-window quota target must be between zero and one")
        if limit["unit"] == "tokens":
            for key in ["max", "reserve"]:
                if key in limit and limit[key] != int(limit[key]):
                    errors.append(f"Token {key} must be an integer")

    policy = plan["task"].get("acceptance_policy", {})
    if policy.get("independent_review") == "script":
        errors.append("Independent model review cannot use the script lane")
    return errors


def main() -> int:
    schemas = {}
    for path in sorted((ROOT / "schema").glob("*.schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(document)
        local_references(document)
        schemas[path.name] = document
        print(f"OK schema: {path.name}")

    plan = json.loads((ROOT / "examples/plan.example.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schemas["plan.schema.json"], format_checker=FormatChecker())
    errors = [f"{list(error.path)}: {error.message}" for error in validator.iter_errors(plan)]
    if not errors:
        errors.extend(semantic_errors(plan))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK example plan: schema and semantic checks")
    print("No task commands executed. Runtime behavior and quota enforcement are not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
