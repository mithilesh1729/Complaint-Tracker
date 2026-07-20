import os
import re
from pathlib import Path

def check_imports():
    src_dir = Path("frontend/src")
    import_re = re.compile(r'import\s+(?:.*?\s+from\s+)?[\'"]([^\'"]+)[\'"]')
    
    errors = 0
    for file_path in src_dir.rglob("*.*"):
        if file_path.suffix not in ['.js', '.jsx', '.ts', '.tsx', '.css']:
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
            
        for match in import_re.finditer(content):
            imp_path = match.group(1)
            if not imp_path.startswith('.'):
                continue
                
            current = file_path.parent.resolve()
            parts = imp_path.replace('\\', '/').split('/')
            
            valid = True
            for part in parts:
                if part == '.' or part == '':
                    continue
                if part == '..':
                    current = current.parent
                    continue
                
                if not current.exists():
                    valid = False
                    break
                    
                actual_items = os.listdir(current)
                
                if part in actual_items:
                    current = current / part
                else:
                    found = False
                    for ext in ['.jsx', '.js', '.css', '.ts', '.tsx']:
                        if f"{part}{ext}" in actual_items:
                            current = current / f"{part}{ext}"
                            found = True
                            break
                    
                    if not found:
                        print(f"CASE MISMATCH: '{imp_path}' in {file_path} -> Cannot find '{part}' in {current}")
                        valid = False
                        errors += 1
                        break
    print(f"Total casing errors found: {errors}")

if __name__ == "__main__":
    check_imports()
