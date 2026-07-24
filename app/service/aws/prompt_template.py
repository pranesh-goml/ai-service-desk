import os
import yaml
from jinja2 import Template

class PromptLoader:
    def render(self, prompt_name: str, **kwargs) -> str:
        # Resolve path to prompts.yaml in the same directory as this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompts_path = os.path.join(base_dir, "prompts.yaml")
        try:
            with open(prompts_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
        except FileNotFoundError:
            # Fallback to current working directory
            with open("prompts.yaml", "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)

        template = Template(prompts[prompt_name]["user"])
        return template.render(**kwargs)
