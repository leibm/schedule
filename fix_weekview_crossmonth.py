import re

def fix(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换 renderWeekView 最后的数据填充块
    old_block = """                const key = this.getMonthKey();
                if (this.scheduleData[key]) {
                    Object.entries(this.scheduleData[key]).forEach(([row, cols]) => {
                        Object.entries(cols).forEach(([col, shift]) => {
                            const cell = document.getElementById(`w-${row}-${col}`);
                            if (cell) { cell.textContent = shift; const wIdx = this.shiftTypes.indexOf(shift); const wStyle = this.getShiftStyle(shift, wIdx); cell.style.background = wStyle.bg; cell.style.color = wStyle.color; cell.style.cssText += this.getUnderlineStyle(shift, !!cell.dataset.wdWeekend); if (cell.dataset.wdWeekend) cell.classList.add('weekend-bg'); }
                        });
                    });
                }"""

    new_block = """                this.defaultStaff.forEach((_, dataRow) => {
                    week.forEach((date) => {
                        const day = date.getDate();
                        const y = date.getFullYear();
                        const m = date.getMonth() + 1;
                        const key = `${y}-${String(m).padStart(2, '0')}`;
                        const shift = this.scheduleData[key]?.[dataRow]?.[day] || '';
                        const cell = document.getElementById(`w-${dataRow}-${day}`);
                        if (cell) {
                            cell.textContent = shift;
                            const wIdx = this.shiftTypes.indexOf(shift);
                            const wStyle = this.getShiftStyle(shift, wIdx);
                            cell.style.background = wStyle.bg;
                            cell.style.color = wStyle.color;
                            cell.style.cssText += this.getUnderlineStyle(shift, !!cell.dataset.wdWeekend);
                            if (cell.dataset.wdWeekend) cell.classList.add('weekend-bg');
                        }
                    });
                });"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] {path}")
    else:
        print(f"[SKIP] {path}: block not found")

if __name__ == '__main__':
    fix('scheduler_v4.html')
    fix('scheduler_mobile.html')
    fix('scheduler_generic.html')
    fix('scheduler_generic_mobile.html')
