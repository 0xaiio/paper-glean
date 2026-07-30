"""Render PlantUML diagrams to PNG images."""
import os
import plantuml
import codecs


def render_all():
    """Render all .puml files in docs/assets/diagrams/ to .png in docs/assets/images/."""
    diagrams_dir = os.path.join(os.path.dirname(__file__), "assets", "diagrams")
    images_dir = os.path.join(os.path.dirname(__file__), "assets", "images")

    os.makedirs(images_dir, exist_ok=True)

    pl = plantuml.PlantUML(url="http://www.plantuml.com/plantuml/img/")

    for filename in os.listdir(diagrams_dir):
        if filename.endswith(".puml"):
            puml_path = os.path.join(diagrams_dir, filename)
            png_path = os.path.join(images_dir, filename.replace(".puml", ".png"))
            try:
                with codecs.open(puml_path, "r", encoding="utf-8") as f:
                    content = f.read()
                result = pl.processes(content)
                with open(png_path, "wb") as f:
                    f.write(result)
                print(f"Rendered: {filename} -> {png_path}")
            except Exception as e:
                print(f"Error rendering {filename}: {e}")


if __name__ == "__main__":
    render_all()
