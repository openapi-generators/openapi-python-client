import subprocess

output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, check=True).stdout

if output == b"":
    # No changes
    exit(0)

print(output)
exit(1)
