import sys, time
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

nb_path = Path(sys.argv[1] if len(sys.argv) > 1 else "mini_project.ipynb").resolve()
nb = nbformat.read(nb_path, as_version=4)
client = NotebookClient(nb, timeout=1800, kernel_name="mini-project",
                        resources={"metadata": {"path": str(nb_path.parent)}})
t0 = time.time()
try:
    client.execute()
    print(f"\n{'='*70}\nRUN ALL PASSED in {time.time()-t0:.1f}s ({len(nb.cells)} cells)\n{'='*70}")
    status = 0
except CellExecutionError:
    idx = next((i for i, c in enumerate(nb.cells)
                if c.get("cell_type") == "code"
                and any(o.get("output_type") == "error" for o in c.get("outputs", []))), None)
    print(f"\n{'='*70}\nFAILED at cell index {idx} after {time.time()-t0:.1f}s\n{'='*70}")
    if idx is not None:
        print("--- SOURCE ---")
        print(nb.cells[idx].source[:2500])
        print("--- ERROR ---")
        for o in nb.cells[idx].outputs:
            if o.get("output_type") == "error":
                print("\n".join(o.get("traceback", []))[-3000:])
    status = 1
finally:
    nbformat.write(nb, nb_path)
sys.exit(status)
