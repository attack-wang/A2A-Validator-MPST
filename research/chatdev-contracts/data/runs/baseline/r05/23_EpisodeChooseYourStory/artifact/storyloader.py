import json
class StoryValidationError(Exception):
    """Raised when a story file fails validation."""
class StoryLoader:
    """Loads story JSON from disk and validates its structure."""
    @staticmethod
    def load(path) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            raise StoryValidationError(f"Story file not found: {path}")
        except json.JSONDecodeError as exc:
            raise StoryValidationError(f"Story file is not valid JSON: {exc}")
        StoryLoader.validate(data, path)
        return data
    @staticmethod
    def validate(data, path="story"):
        if not isinstance(data, dict):
            raise StoryValidationError(f"{path}: top level must be an object")
        nodes = data.get("nodes")
        if not isinstance(nodes, dict) or not nodes:
            raise StoryValidationError(f"{path}: 'nodes' must be a non-empty object")
        start = data.get("start")
        if not start or start not in nodes:
            raise StoryValidationError(f"{path}: 'start' must name an existing node")
        # Collect every target reference and check it exists.
        for node_id, node in nodes.items():
            if not isinstance(node, dict):
                raise StoryValidationError(f"{path}: node '{node_id}' must be an object")
            choices = node.get("choices", [])
            if not node.get("is_ending", False) and not choices:
                raise StoryValidationError(
                    f"{path}: non-ending node '{node_id}' has no choices (dead end)"
                )
            if node.get("is_ending", False) and not node.get("ending_id"):
                raise StoryValidationError(
                    f"{path}: ending node '{node_id}' is missing 'ending_id'"
                )
            for i, choice in enumerate(choices):
                target = choice.get("target")
                if target not in nodes:
                    raise StoryValidationError(
                        f"{path}: node '{node_id}' choice #{i} targets unknown node '{target}'"
                    )