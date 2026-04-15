import re

def cleanup(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all renderTemplatePersonSelect definitions
    pattern1 = re.compile(
        r"\s+renderTemplatePersonSelect\(\) \{"
        r"\s+const sel = document\.getElementById\('templatePerson'\);"
        r"\s+if \(!sel\) return;"
        r"\s+const current = sel\.value;"
        r"\s+sel\.innerHTML = '<option value=\"\">选择人员</option>';"
        r"\s+const staffList = this\.getStaffList\(\);"
        r"\s+this\.defaultStaff\.forEach\(\(_, i\) => \{"
        r"\s+const opt = document\.createElement\('option'\);"
        r"\s+opt\.value = i;"
        r"\s+opt\.textContent = staffList\[i\];"
        r"\s+sel\.appendChild\(opt\);"
        r"\s+\}\);"
        r"\s+sel\.value = current;"
        r"\s+\},",
        re.DOTALL
    )
    content = pattern1.sub("", content)

    # 2. Remove applyTemplate method
    pattern2 = re.compile(
        r"\s+applyTemplate\(\) \{ const rowIndex = parseInt\(document\.getElementById\('templatePerson'\)\.value, 10\);"
        r" const startDay = parseInt\(document\.getElementById\('templateStart'\)\.value\) \|\| 1;"
        r" const patternStr = document\.getElementById\('templatePattern'\)\.value\.trim\(\);"
        r" if \(isNaN\(rowIndex\)\) \{ alert\('请选择人员'\); return; \}"
        r" const pattern = patternStr\.split\(/\[,\，\]/\)\.map\(s => s\.trim\(\)\)\.filter\(s => s\);"
        r" if \(pattern\.length === 0\) \{ alert\('模板格式错误'\); return; \}"
        r" for \(let day = 1; day <= this\.daysInMonth; day\+\+\) \{"
        r" const offset = day - startDay;"
        r" const patternIndex = \(\(offset % pattern\.length\) \+ pattern\.length\) % pattern\.length;"
        r" const shift = pattern\[patternIndex\];"
        r" if \(this\.shiftTypes\.includes\(shift\)\) this\.setShift\(rowIndex, day, shift, true\); \}"
        r" this\.updateStats\(\); localStorage\.setItem\('scheduleData_generic_v2', JSON\.stringify\(this\.scheduleData\)\);"
        r" alert\('模板已应用！'\); \},"
    )
    content = pattern2.sub("", content)

    # 3. Remove templatePattern default setter lines
    content = re.sub(r"\s+document\.getElementById\('templatePattern'\)\.value = [^;]+;\n", "\n", content)

    # 4. Remove renderTemplatePersonSelect calls
    content = re.sub(r"\s+this\.renderTemplatePersonSelect\(\);", "", content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    cleanup('scheduler_generic.html')
    cleanup('scheduler_generic_mobile.html')
