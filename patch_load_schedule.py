import re

def patch(path, storage_key):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add load button after saveSchedule / exportExcel group
    old_btn = '''                <button class="btn-secondary" onclick="window.print()">🖨️</button>
            </div>'''
    new_btn = '''                <button class="btn-secondary" onclick="window.print()">🖨️</button>
            </div>
            <div class="toolbar-group">
                <button class="btn-primary" onclick="app.loadSchedule()">📥 加载</button>
            </div>'''
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
    else:
        print(f"[WARN] {path}: button anchor not found")

    # 2. Add loadSchedule method after saveSchedule
    old_js = f"""            saveSchedule() {{ const data = {{ version: '2.0', exportDate: new Date().toISOString(), staff: this.defaultStaff, schedules: this.scheduleData }}; const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `排班数据_${{this.getMonthKey()}}.json`; a.click(); URL.revokeObjectURL(url); localStorage.setItem('{storage_key}', JSON.stringify(this.scheduleData)); alert('排班已保存！'); }},"""
    new_js = f"""            saveSchedule() {{ const data = {{ version: '2.0', exportDate: new Date().toISOString(), staff: this.defaultStaff, schedules: this.scheduleData }}; const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `排班数据_${{this.getMonthKey()}}.json`; a.click(); URL.revokeObjectURL(url); localStorage.setItem('{storage_key}', JSON.stringify(this.scheduleData)); alert('排班已保存！'); }},
            loadSchedule() {{
                let input = document.getElementById('scheduleFileInput');
                if (!input) {{
                    input = document.createElement('input');
                    input.type = 'file';
                    input.id = 'scheduleFileInput';
                    input.accept = '.json,application/json';
                    input.style.display = 'none';
                    input.onchange = (e) => {{
                        const file = e.target.files[0];
                        if (!file) return;
                        const reader = new FileReader();
                        reader.onload = (ev) => {{
                            try {{
                                const data = JSON.parse(ev.target.result);
                                if (!data || !data.schedules) {{ alert('文件格式错误'); return; }}
                                if (confirm('加载排班会覆盖当前所有月份的数据，是否继续？')) {{
                                    this.scheduleData = {{ ...this.scheduleData, ...data.schedules }};
                                    localStorage.setItem('{storage_key}', JSON.stringify(this.scheduleData));
                                    this.loadMonthData();
                                    alert('排班已加载！');
                                }}
                            }} catch (err) {{ alert('文件解析失败：' + err.message); }}
                        }};
                        reader.readAsText(file);
                    }};
                    document.body.appendChild(input);
                }}
                input.click();
            }},"""
    if old_js in content:
        content = content.replace(old_js, new_js)
    else:
        print(f"[WARN] {path}: JS anchor not found")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch('scheduler_v4.html', 'scheduleData_v2')
    patch('scheduler_mobile.html', 'scheduleData_v2')
    patch('scheduler_generic.html', 'scheduleData_generic_v2')
    patch('scheduler_generic_mobile.html', 'scheduleData_generic_v2')
