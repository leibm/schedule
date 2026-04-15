import re

OLD_HOLIDAYS = """            holidays: {
                '2025-01-01': '元旦', '2025-01-28': '春节', '2025-01-29': '春节', '2025-01-30': '春节',
                '2025-01-31': '春节', '2025-02-01': '春节', '2025-02-02': '春节', '2025-02-03': '春节',
                '2025-02-04': '春节', '2025-04-04': '清明', '2025-04-05': '清明', '2025-04-06': '清明',
                '2025-05-01': '劳动', '2025-05-02': '劳动', '2025-05-03': '劳动', '2025-05-04': '劳动',
                '2025-05-05': '劳动', '2025-05-31': '端午', '2025-06-01': '端午', '2025-06-02': '端午',
                '2025-10-01': '国庆', '2025-10-02': '国庆', '2025-10-03': '国庆', '2025-10-04': '国庆',
                '2025-10-05': '国庆', '2025-10-06': '国庆', '2025-10-07': '国庆', '2025-10-08': '国庆',
                '2026-01-01': '元旦', '2026-02-17': '春节', '2026-02-18': '春节', '2026-02-19': '春节',
                '2026-02-20': '春节', '2026-02-21': '春节', '2026-02-22': '春节', '2026-02-23': '春节',
                '2026-02-24': '春节', '2026-04-04': '清明', '2025-04-05': '清明', '2025-04-06': '清明',
                '2026-05-01': '劳动', '2026-05-02': '劳动', '2026-05-03': '劳动', '2026-05-04': '劳动',
                '2026-05-05': '劳动', '2026-06-19': '端午', '2026-06-20': '端午', '2026-06-21': '端午',
                '2026-09-25': '中秋', '2026-09-26': '中秋', '2026-09-27': '中秋',
                '2026-10-01': '国庆', '2026-10-02': '国庆', '2026-10-03': '国庆', '2026-10-04': '国庆',
                '2026-10-05': '国庆', '2026-10-06': '国庆', '2026-10-07': '国庆', '2026-10-08': '国庆'
            },"""

NEW_HOLIDAYS = """            holidays: {
                // 2025 法定节假日
                '2025-01-01': { name: '元旦', off: true },
                '2025-01-28': { name: '春节', off: true }, '2025-01-29': { name: '春节', off: true }, '2025-01-30': { name: '春节', off: true },
                '2025-01-31': { name: '春节', off: true }, '2025-02-01': { name: '春节', off: true }, '2025-02-02': { name: '春节', off: true },
                '2025-02-03': { name: '春节', off: true }, '2025-02-04': { name: '春节', off: true },
                '2025-04-04': { name: '清明', off: true }, '2025-04-05': { name: '清明', off: true }, '2025-04-06': { name: '清明', off: true },
                '2025-05-01': { name: '劳动', off: true }, '2025-05-02': { name: '劳动', off: true }, '2025-05-03': { name: '劳动', off: true },
                '2025-05-04': { name: '劳动', off: true }, '2025-05-05': { name: '劳动', off: true },
                '2025-05-31': { name: '端午', off: true }, '2025-06-01': { name: '端午', off: true }, '2025-06-02': { name: '端午', off: true },
                '2025-10-01': { name: '国庆', off: true }, '2025-10-02': { name: '国庆', off: true }, '2025-10-03': { name: '国庆', off: true },
                '2025-10-04': { name: '国庆', off: true }, '2025-10-05': { name: '国庆', off: true }, '2025-10-06': { name: '国庆', off: true },
                '2025-10-07': { name: '国庆', off: true }, '2025-10-08': { name: '国庆', off: true },
                // 2025 非放假节日
                '2025-02-12': { name: '元宵', off: false }, '2025-02-14': { name: '情人节', off: false },
                '2025-03-08': { name: '妇女节', off: false }, '2025-04-01': { name: '愚人节', off: false },
                '2025-05-11': { name: '母亲节', off: false }, '2025-05-12': { name: '护士节', off: false },
                '2025-06-01': { name: '儿童节', off: false }, '2025-06-15': { name: '父亲节', off: false },
                '2025-08-29': { name: '七夕', off: false }, '2025-09-06': { name: '中元', off: false },
                '2025-09-10': { name: '教师节', off: false }, '2025-10-29': { name: '重阳', off: false },
                '2025-10-31': { name: '万圣', off: false }, '2025-12-24': { name: '平安夜', off: false },
                '2025-12-25': { name: '圣诞', off: false },
                // 2026 法定节假日
                '2026-01-01': { name: '元旦', off: true },
                '2026-02-17': { name: '春节', off: true }, '2026-02-18': { name: '春节', off: true }, '2026-02-19': { name: '春节', off: true },
                '2026-02-20': { name: '春节', off: true }, '2026-02-21': { name: '春节', off: true }, '2026-02-22': { name: '春节', off: true },
                '2026-02-23': { name: '春节', off: true }, '2026-02-24': { name: '春节', off: true },
                '2026-04-04': { name: '清明', off: true }, '2026-04-05': { name: '清明', off: true }, '2026-04-06': { name: '清明', off: true },
                '2026-05-01': { name: '劳动', off: true }, '2026-05-02': { name: '劳动', off: true }, '2026-05-03': { name: '劳动', off: true },
                '2026-05-04': { name: '劳动', off: true }, '2026-05-05': { name: '劳动', off: true },
                '2026-06-19': { name: '端午', off: true }, '2026-06-20': { name: '端午', off: true }, '2026-06-21': { name: '端午', off: true },
                '2026-09-25': { name: '中秋', off: true }, '2026-09-26': { name: '中秋', off: true }, '2026-09-27': { name: '中秋', off: true },
                '2026-10-01': { name: '国庆', off: true }, '2026-10-02': { name: '国庆', off: true }, '2026-10-03': { name: '国庆', off: true },
                '2026-10-04': { name: '国庆', off: true }, '2026-10-05': { name: '国庆', off: true }, '2026-10-06': { name: '国庆', off: true },
                '2026-10-07': { name: '国庆', off: true }, '2026-10-08': { name: '国庆', off: true },
                // 2026 非放假节日
                '2026-02-14': { name: '情人节', off: false }, '2026-03-03': { name: '元宵', off: false },
                '2026-03-08': { name: '妇女节', off: false }, '2026-04-01': { name: '愚人节', off: false },
                '2026-05-10': { name: '母亲节', off: false }, '2026-05-12': { name: '护士节', off: false },
                '2026-06-01': { name: '儿童节', off: false }, '2026-06-21': { name: '父亲节', off: false },
                '2026-09-17': { name: '七夕', off: false }, '2026-09-25': { name: '中元', off: false },
                '2026-09-10': { name: '教师节', off: false }, '2026-10-18': { name: '重阳', off: false },
                '2026-10-31': { name: '万圣', off: false }, '2026-12-24': { name: '平安夜', off: false },
                '2026-12-25': { name: '圣诞', off: false }
            },"""

CSS_ADDITION = """        .schedule-table th.festival {
            background: #e6f7ff;
            color: #096dd9;
        }

        .day-cell.festival {
            background: #f0faff;
        }

        .day-number.festival-day {
            color: #096dd9;
            font-weight: 600;
        }
"""

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_HOLIDAYS not in content:
        print(f"[SKIP] {path}: holidays block not found")
        return

    content = content.replace(OLD_HOLIDAYS, NEW_HOLIDAYS)

    # Insert CSS after the last .day-number.holiday-day block
    css_anchor = """        .day-number.holiday-day {
            color: #a8071a;
        }"""
    if css_anchor in content and '.schedule-table th.festival' not in content:
        content = content.replace(css_anchor, css_anchor + '\n\n' + CSS_ADDITION)
    else:
        print(f"[WARN] {path}: CSS anchor not found or already patched")

    # Replace class names and display strings
    # holiday ? 'holiday' : ''   ->   holiday ? (holiday.off ? 'holiday' : 'festival') : ''
    content = re.sub(r"(?<![\w.])holiday \? 'holiday' : ''", "holiday ? (holiday.off ? 'holiday' : 'festival') : ''", content)

    # holiday ? 'holiday-day' : ''   ->   holiday ? (holiday.off ? 'holiday-day' : 'festival-day') : ''
    content = re.sub(r"(?<![\w.])holiday \? 'holiday-day' : ''", "holiday ? (holiday.off ? 'holiday-day' : 'festival-day') : ''", content)

    # holiday ? ' ' + holiday : ''   ->   holiday ? ' ' + holiday.name : ''
    content = re.sub(r"(?<![\w.])holiday \? ' ' \+ holiday : ''", "holiday ? ' ' + holiday.name : ''", content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch_file('scheduler_v4.html')
    patch_file('影像科月度排班系统_手机版.html')
