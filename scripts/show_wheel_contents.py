"""Display the contents of all wheel files in the dist/ directory."""
import os
import zipfile


dist_files = sorted(f for f in os.listdir("dist") if f.endswith(".whl"))
for whl in dist_files:
    print(f"Wheel: {whl}")
    with zipfile.ZipFile(os.path.join("dist", whl)) as z:
        for name in sorted(z.namelist()):
            print(f"  {name}")
