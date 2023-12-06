import subprocess
import sys

output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, check=True).stdout

if output == b"":
    # No changes
    sys.exit(0)

print(output)
sys.exit(1)
