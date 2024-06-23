from jinja2 import Template


def load_template(template_path: str) -> Template:
    with open(template_path, encoding="utf-8") as file:
        template_content = file.read()
    return Template(template_content)
