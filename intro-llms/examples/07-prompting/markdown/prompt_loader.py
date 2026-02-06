from pathlib import Path

class PromptLoader:
    def __init__(self, base_path: str = "prompts"):
        # Resolve path relative to this file's location, not the working directory
        self.base = Path(__file__).parent / base_path
    
    def load(self, name: str) -> str:
        return (self.base / name).read_text()
    
    def build_prompt(self, issue_id: str, title: str, description: str) -> list[dict]:
        system = self.load("system.md")
        examples = self.load("examples.md")
        template = self.load("user.md")
        return [
            {"role": "developer", "content": system + "\n" + examples},
            {"role": "user", "content": template.format(issue_id=issue_id, title=title, description=description)}
        ]
