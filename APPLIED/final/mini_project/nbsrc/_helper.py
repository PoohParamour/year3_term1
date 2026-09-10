"""Notebook builder helpers: assemble mini_project.ipynb from section files."""
import nbformat as nbf

def md(text):
    return nbf.v4.new_markdown_cell(text.strip("\n"))

def code(text):
    return nbf.v4.new_code_cell(text.strip("\n"))

def build(cells, path, kernel="mini-project", display="Python (mini-project)"):
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata = {
        "kernelspec": {"name": kernel, "display_name": display, "language": "python"},
        "language_info": {"name": "python"},
    }
    nbf.write(nb, path)
    return len(cells)
