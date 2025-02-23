import openai
import os
import subprocess
import requests
import re
from openai import OpenAI

def get_last_build_error():
    """Reads the last pipeline error log from errors.txt"""
    try:
        with open("errors.txt", "r") as file:
            errors = file.read().strip()
            return errors if errors else "No error logs captured."
    except Exception as e:
        return f"Failed to retrieve error logs: {str(e)}"

def extract_error_file(error_log):
    """Extracts the filename and line number from the error log"""
    match = re.search(r'File "(.*)", line (\d+)', error_log)
    if match:
        return match.group(1), int(match.group(2))
    return "app.py", 1  # Default to app.py if not found

def suggest_fix_llama3_70(error_log):   
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key="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",
    )

    completion = client.chat.completions.create(
      model="meta-llama/llama-3.1-405b-instruct",
      messages=[{"role": "user", "content": "Please fix the following Flask error:\n" + error_log}]
    )
    return completion.choices[0].message.content

def apply_fix(fix_suggestion, file_path):
    """Applies the fix suggested by OpenAI to the correct file"""
    try:
        with open(file_path, "w") as f:
            f.write(fix_suggestion)
        return True
    except Exception as e:
        print(f"Failed to apply fix: {str(e)}")
        return False

# Main script execution
error_log = get_last_build_error()
if "No error logs" in error_log:
    print("No errors detected.")
    exit(0)

file_path, line_number = extract_error_file(error_log)
print(f"Detected issue in: {file_path} at line {line_number}")

fix_suggestion = suggest_fix_llama3_70(error_log)
print("Suggested Fix:\n", fix_suggestion)

if apply_fix(fix_suggestion, file_path):
    print(f"Fix applied to {file_path}. Committing changes...")
    subprocess.run(f"git add {file_path}", shell=True)
    subprocess.run('git commit -m "Auto-fixed Flask error"', shell=True)
    subprocess.run("git push origin main", shell=True)
else:
    print("Failed to apply the fix.")
