import json
from pathlib import Path

INTENTS_DIR = Path(__file__).resolve().parent.parent / "intents"
REQUIRED_TOP_LEVEL = ["intent", "description", "examples", "behavior"]


class IntentLoadError(Exception):
    pass


def _validate_behavior_state(state, filename, path):
    if "responses" not in state:
        raise IntentLoadError(f"{filename}: {path} missing 'responses'")
    if not isinstance(state["responses"], list) or len(state["responses"]) < 1:
        raise IntentLoadError(f"{filename}: {path}.responses must be a non-empty list")
    if "action" not in state:
        raise IntentLoadError(f"{filename}: {path} missing 'action' (use null if none)")


def _validate_structure(data, filename):
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            raise IntentLoadError(f"{filename}: missing required field '{key}'")

    for i, example in enumerate(data["examples"]):
        if "text" not in example:
            raise IntentLoadError(f"{filename}: examples[{i}] missing 'text'")

    behavior = data["behavior"]
    if "responses" in behavior:
        _validate_behavior_state(behavior, filename, "behavior")
    else:
        for state_name, state_body in behavior.items():
            _validate_behavior_state(state_body, filename, f"behavior.{state_name}")


def load_all_intents(intents_dir=INTENTS_DIR):
    intents = {}
    for filepath in sorted(intents_dir.glob("*.json")):
        with open(filepath) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise IntentLoadError(f"{filepath.name}: invalid JSON -- {e}")
        _validate_structure(data, filepath.name)
        intents[data["intent"]] = data
    return intents


if __name__ == "__main__":
    loaded = load_all_intents()
    print(f"Loaded {len(loaded)} intents: {list(loaded.keys())}")