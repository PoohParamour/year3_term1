import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _helper import build

SECTIONS = ["s0_setup", "s1_business", "s2_understanding", "s3_preparation",
            "s4a_basket", "s4b_segmentation", "s4c_churn",
            "s5_evaluation", "s6_deployment"]

cells = []
used = []
for name in SECTIONS:
    try:
        mod = importlib.import_module(name)
    except ModuleNotFoundError:
        continue
    importlib.reload(mod)
    cells.extend(mod.CELLS)
    used.append(f"{name}({len(mod.CELLS)})")

out = Path(__file__).resolve().parent.parent / "mini_project.ipynb"
n = build(cells, out)
print(f"built {n} cells from: {', '.join(used)}")
print(f"-> {out}")
