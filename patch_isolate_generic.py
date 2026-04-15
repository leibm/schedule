import os
import re

replacements = {
    "customStaff_v1": "customStaff_generic_v1",
    "customShifts_v1": "customShifts_generic_v1",
    "scheduleData_v2": "scheduleData_generic_v2",
    "staffOrder_v2": "staffOrder_generic_v2",
}

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch_file('scheduler_generic.html')
    patch_file('scheduler_generic_mobile.html')
