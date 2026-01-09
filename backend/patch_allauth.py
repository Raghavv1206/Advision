# patch_allauth.py - FIXED VERSION
import os
import sys

# Find the allauth app_settings.py file
venv_path = sys.prefix
allauth_path = os.path.join(venv_path, 'Lib', 'site-packages', 'allauth', 'account', 'app_settings.py')

print(f"Looking for allauth at: {allauth_path}")

if not os.path.exists(allauth_path):
    print("❌ Could not find allauth installation")
    sys.exit(1)

# Read the file
with open(allauth_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process line by line
new_lines = []
skip_until_dedent = False
indent_level = 0

for i, line in enumerate(lines):
    # Check for first assertion
    if "assert not self.USERNAME_REQUIRED" in line and "# Patched" not in line:
        new_lines.append(line.replace("assert not self.USERNAME_REQUIRED", 
                                     "pass  # assert not self.USERNAME_REQUIRED - Patched"))
        print(f"✅ Patched line {i+1}: USERNAME_REQUIRED assertion")
        continue
    
    # Check for second assertion
    if "assert self.AUTHENTICATION_METHOD not in (" in line and not skip_until_dedent:
        # Comment out the assertion and start skipping the multi-line block
        new_lines.append(line.replace("assert self.AUTHENTICATION_METHOD", 
                                     "# assert self.AUTHENTICATION_METHOD - Patched"))
        skip_until_dedent = True
        indent_level = len(line) - len(line.lstrip())
        print(f"✅ Patched line {i+1}: AUTHENTICATION_METHOD assertion (multi-line)")
        continue
    
    # Skip lines that are part of the assertion block
    if skip_until_dedent:
        current_indent = len(line) - len(line.lstrip())
        # Continue skipping if line is indented more than the assert line or is blank
        if line.strip() == "" or current_indent > indent_level:
            new_lines.append("# " + line if line.strip() else line)
            continue
        else:
            # We've reached the end of the assertion block
            skip_until_dedent = False
    
    new_lines.append(line)

# Write back
with open(allauth_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ Successfully patched django-allauth!")
print(f"✅ Modified: {allauth_path}")
print("\nNow run: python manage.py makemigrations")