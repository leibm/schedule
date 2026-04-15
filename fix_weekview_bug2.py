import re

def fix(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern 1: in loadMonthData / prevWeek / nextWeek
    # Replace: if (this.scheduleData[key]) this.applyScheduleData(this.scheduleData[key]);
    # With:    if (this.scheduleData[key] && this.currentView !== 'week') this.applyScheduleData(this.scheduleData[key]);
    old = "if (this.scheduleData[key]) this.applyScheduleData(this.scheduleData[key]);"
    new = "if (this.scheduleData[key] && this.currentView !== 'week') this.applyScheduleData(this.scheduleData[key]);"

    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"[OK] {path}: replaced {count} occurrence(s)")
    else:
        print(f"[SKIP] {path}: pattern not found")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix('scheduler_v4.html')
    fix('scheduler_mobile.html')
    fix('scheduler_generic.html')
    fix('scheduler_generic_mobile.html')
