import os
import subprocess
import sys

project_dir = r"c:\Users\sharath V\Vimal Project\AI_Bootcamp\AI_Interview_Assistant"
os.chdir(project_dir)
result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], check=False)
sys.exit(result.returncode)
