import subprocess

def run_cmd(command: str) -> str:
  result = subprocess.run(command, shell=True, capture_output=True, text=True)
  return result.stdout
