import re

def modify(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Remove range button
    c = c.replace('<button onclick="app.setView(\'range\')">📆 范围</button>\n', '')

    # 2. Range picker always visible + clear button
    c = c.replace(
        '<div class="toolbar-group" id="rangePickerGroup" style="display:none;">\n'
        '                <label>开始</label>\n'
        '                <input type="date" id="rangeStart" onchange="app.onRangeChange()">\n'
        '                <label>结束</label>\n'
        '                <input type="date" id="rangeEnd" onchange="app.onRangeChange()">\n'
        '            </div>',
        '<div class="toolbar-group" id="rangePickerGroup">\n'
        '                <label>范围</label>\n'
        '                <input type="date" id="rangeStart" onchange="app.onRangeChange()">\n'
        '                <input type="date" id="rangeEnd" onchange="app.onRangeChange()">\n'
        '                <button class="btn-secondary" onclick="app.clearRange()">整月</button>\n'
        '            </div>')

    # 3. Template select hardcoded options -> only placeholder
    c = c.replace(
        '                    <select id="templatePerson">\n'
        '                        <option value="">选择人员</option>\n'
        '                        <option value="向锺宁">向锺宁</option>\n'
        '                        <option value="陈钰波">陈钰波</option>\n'
        '                        <option value="刘成伟">刘成伟</option>\n'
        '                        <option value="刘浅予">刘浅予</option>\n'
        '                        <option value="雷宝铭">雷宝铭</option>\n'
        '                        <option value="丁小涵">丁小涵</option>\n'
        '                        <option value="徐畅">徐畅</option>\n'
        '                    </select>',
        '                    <select id="templatePerson">\n'
        '                        <option value="">选择人员</option>\n'
        '                    </select>')

    # 4. Remove rangeView DOM block
    c = c.replace(
        '        <div class="range-view" id="rangeView">\n'
        '            <div class="range-toolbar">\n'
        '                <span id="rangeLabel"></span>\n'
        '            </div>\n'
        '            <div class="table-wrapper" style="display:block;">\n'
        '                <table class="schedule-table" id="rangeTable">\n'
        '                    <thead id="rangeHead"></thead>\n'
        '                    <tbody id="rangeBody"></tbody>\n'
        '                </table>\n'
        '            </div>\n'
        '        </div>\n', '')

    # 5. CSS cleanup
    c = c.replace(
        '        .range-view {\n'
        '            display: none;\n'
        '        }\n\n'
        '        .range-view.active {\n'
        '            display: block;\n'
        '        }\n\n'
        '        .week-toolbar,\n'
        '        .range-toolbar {\n'
        '            display: flex;\n'
        '            justify-content: space-between;\n'
        '            align-items: center;\n'
        '            margin-bottom: 12px;\n'
        '            padding: 10px 12px;\n'
        '            background: #f8f9fa;\n'
        '            border-radius: 8px;\n'
        '            gap: 8px;\n'
        '        }\n\n'
        '        .week-toolbar span,\n'
        '        .range-toolbar span {\n'
        '            font-weight: 500;\n'
        '            color: #333;\n'
        '            font-size: 14px;\n'
        '            flex: 1;\n'
        '            text-align: center;\n'
        '        }',
        '        .week-toolbar {\n'
        '            display: flex;\n'
        '            justify-content: space-between;\n'
        '            align-items: center;\n'
        '            margin-bottom: 12px;\n'
        '            padding: 10px 12px;\n'
        '            background: #f8f9fa;\n'
        '            border-radius: 8px;\n'
        '            gap: 8px;\n'
        '        }\n\n'
        '        .week-toolbar span {\n'
        '            font-weight: 500;\n'
        '            color: #333;\n'
        '            font-size: 14px;\n'
        '            flex: 1;\n'
        '            text-align: center;\n'
        '        }')

    # 6. Remove default range values in init()
    c = c.replace(
        "                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;\n"
        "                const now = new Date();\n"
        "                const fmt = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;\n"
        "                document.getElementById('rangeStart').value = fmt(now);\n"
        "                const end = new Date(now); end.setDate(end.getDate() + 6);\n"
        "                document.getElementById('rangeEnd').value = fmt(end);\n"
        "                const savedOrder = localStorage.getItem('staffOrder_v2');",
        "                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;\n"
        "                const savedOrder = localStorage.getItem('staffOrder_v2');")

    # 7. init: add renderTemplatePersonSelect before loadMonthData
    c = c.replace(
        'this.renderStatsSelect();\n                this.loadMonthData();',
        'this.renderStatsSelect();\n                this.renderTemplatePersonSelect();\n                this.loadMonthData();')

    # 8. moveStaff/dragStaff re-render template select
    c = c.replace(
        "localStorage.setItem('staffOrder_v2', JSON.stringify(list));\n                this.loadMonthData();",
        "localStorage.setItem('staffOrder_v2', JSON.stringify(list));\n                this.renderTemplatePersonSelect();\n                this.loadMonthData();")

    # 9. setView remove range logic
    c = c.replace(
        '            setView(view) {\n'
        '                this.currentView = view;\n'
        "                document.querySelectorAll('.view-toggle button').forEach((btn, i) => {\n"
        "                    btn.classList.toggle('active', (view === 'table' && i === 0) || (view === 'card' && i === 1) || (view === 'week' && i === 2) || (view === 'range' && i === 3));\n"
        '                });\n'
        "                document.getElementById('tableView').classList.toggle('active', view === 'table');\n"
        "                document.getElementById('cardView').classList.toggle('active', view === 'card');\n"
        "                document.getElementById('weekView').classList.toggle('active', view === 'week');\n"
        "                document.getElementById('rangeView').classList.toggle('active', view === 'range');\n"
        "                document.getElementById('rangePickerGroup').style.display = view === 'range' ? 'flex' : 'none';\n"
        "                if (view === 'week') this.renderWeekView();\n"
        "                if (view === 'range') this.renderRangeView();\n"
        '            },',
        '            setView(view) {\n'
        '                this.currentView = view;\n'
        "                document.querySelectorAll('.view-toggle button').forEach((btn, i) => {\n"
        "                    btn.classList.toggle('active', (view === 'table' && i === 0) || (view === 'card' && i === 1) || (view === 'week' && i === 2));\n"
        '                });\n'
        "                document.getElementById('tableView').classList.toggle('active', view === 'table');\n"
        "                document.getElementById('cardView').classList.toggle('active', view === 'card');\n"
        "                document.getElementById('weekView').classList.toggle('active', view === 'week');\n"
        "                if (view === 'week') this.renderWeekView();\n"
        '            },')

    # 10. loadMonthData remove renderRangeView
    c = c.replace(
        "                if (this.currentView === 'week') this.renderWeekView();\n"
        "                if (this.currentView === 'range') this.renderRangeView();\n"
        "                const key = this.getMonthKey();",
        "                if (this.currentView === 'week') this.renderWeekView();\n"
        "                const key = this.getMonthKey();")

    # 11. Regex replace renderTable block and prepend getTableDates
    pattern = re.compile(r'            renderTable\(\) \{.*?\n            \},', re.DOTALL)
    m = pattern.search(c)
    if m:
        new_block = (
            '            getTableDates() {\n'
            "                const startVal = document.getElementById('rangeStart').value;\n"
            "                const endVal = document.getElementById('rangeEnd').value;\n"
            '                const dates = [];\n'
            '                if (!startVal || !endVal) {\n'
            '                    for (let d = 1; d <= this.daysInMonth; d++) dates.push(new Date(this.currentYear, this.currentMonth - 1, d));\n'
            '                    return dates;\n'
            '                }\n'
            '                let start = new Date(startVal);\n'
            '                let end = new Date(endVal);\n'
            '                if (start > end) { [start, end] = [end, start]; }\n'
            '                const diffDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));\n'
            '                if (diffDays > 30) {\n'
            '                    end = new Date(start); end.setDate(end.getDate() + 30);\n'
            "                    const fmt = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;\n"
            "                    document.getElementById('rangeEnd').value = fmt(end);\n"
            '                }\n'
            '                for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) dates.push(new Date(d));\n'
            '                return dates;\n'
            '            },\n'
            '            renderTable() {\n'
            "                const thead = document.getElementById('tableHead'), tbody = document.getElementById('tableBody');\n"
            "                const weekNames = ['日', '一', '二', '三', '四', '五', '六'];\n"
            '                const dates = this.getTableDates();\n'
            '                const isCurrentMonthOnly = dates.every(d => d.getFullYear() === this.currentYear && d.getMonth() + 1 === this.currentMonth);\n'
            '                let headHTML = \'<tr><th class="name-header">姓名</th>\';\n'
            '                dates.forEach(date => {\n'
            '                    const d = date.getDate();\n'
            '                    const wd = date.getDay();\n'
            '                    const holiday = this.isHoliday(date.getFullYear(), date.getMonth() + 1, d);\n'
            "                    const cls = [wd === 0 || wd === 6 ? 'weekend' : '', holiday ? 'holiday' : ''].filter(Boolean).join(' ');\n"
            "                    const label = isCurrentMonthOnly ? d : `${date.getMonth() + 1}/${d}`;\n"
            "                    headHTML += `<th class=\"${cls}\">${label}<br><small>周${weekNames[wd]}${holiday ? ' ' + holiday : ''}</small></th>`;\n"
            '                });\n'
            '                headHTML += \'</tr>\';\n'
            '                thead.innerHTML = headHTML;\n'
            "                tbody.innerHTML = '';\n"
            '                const staffList = this.getStaffList();\n'
            '                this.defaultStaff.forEach((_, dataRow) => {\n'
            '                    const name = staffList[dataRow];\n'
            "                    const tr = document.createElement('tr');\n"
            "                    const nameTd = document.createElement('td');\n"
            "                    nameTd.className = 'name-cell';\n"
            '                    nameTd.textContent = name;\n'
            '                    this.bindDragEvents(nameTd, dataRow);\n'
            '                    tr.appendChild(nameTd);\n'
            '                    dates.forEach(date => {\n'
            '                        const y = date.getFullYear(), m = date.getMonth() + 1, d = date.getDate();\n'
            '                        const wd = date.getDay();\n'
            "                        const td = document.createElement('td');\n"
            "                        td.className = 'shift-cell';\n"
            "                        if (wd === 0 || wd === 6) td.classList.add('weekend-bg');\n"
            '                        if (isCurrentMonthOnly) {\n'
            '                            td.id = `t-${dataRow}-${d}`;\n'
            "                            td.addEventListener('click', () => this.setShift(dataRow, d, this.currentShift));\n"
            '                        } else {\n'
            "                            const key = `${y}-${String(m).padStart(2, '0')}`;\n"
            '                            const shift = this.scheduleData[key]?.[dataRow]?.[d] || \'\';\n'
            '                            td.textContent = shift;\n'
            "                            td.classList.add('shift-' + (shift || 'empty'));\n"
            "                            td.addEventListener('click', () => {\n"
            '                                const origYear = this.currentYear, origMonth = this.currentMonth, origDays = this.daysInMonth;\n'
            '                                this.currentYear = y; this.currentMonth = m; this.daysInMonth = this.getDaysInMonth(y, m);\n'
            '                                this.setShift(dataRow, d, this.currentShift);\n'
            '                                this.currentYear = origYear; this.currentMonth = origMonth; this.daysInMonth = origDays;\n'
            '                            });\n'
            '                        }\n'
            '                        tr.appendChild(td);\n'
            '                    });\n'
            '                    tbody.appendChild(tr);\n'
            '                });\n'
            '            },'
        )
        c = c[:m.start()] + new_block + c[m.end():]
        print('Replaced renderTable in', path)
    else:
        print('WARN: renderTable not found in', path)

    # 12. onRangeChange
    c = c.replace(
        '            onRangeChange() {\n'
        "                if (this.currentView === 'range') this.renderRangeView();\n"
        '            },',
        '            onRangeChange() {\n'
        "                if (this.currentView === 'table') this.renderTable();\n"
        '            },')

    # 13. Remove renderRangeView method
    pattern2 = re.compile(r'            renderRangeView\(\) \{.*?\n            \},\n            prevWeek\(\) \{', re.DOTALL)
    m2 = pattern2.search(c)
    if m2:
        c = c[:m2.start()] + '            prevWeek() {' + c[m2.end():]
        print('Removed renderRangeView in', path)
    else:
        print('WARN: renderRangeView not found in', path)

    # 14. setShift cross-month redraw
    c = c.replace(
        "                if (!skipSave) { this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData)); }\n"
        '            },\n'
        '            updateSummary(row) {',
        "                if (!skipSave) {\n"
        "                    this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData));\n"
        "                    if (this.currentView === 'table') {\n"
        '                        const dates = this.getTableDates();\n'
        '                        const isCrossMonth = dates.some(d => d.getFullYear() !== this.currentYear || d.getMonth() + 1 !== this.currentMonth);\n'
        "                        if (isCrossMonth) this.renderTable();\n"
        '                    }\n'
        '                }\n'
        '            },\n'
        '            updateSummary(row) {')

    # 15. Add renderTemplatePersonSelect after renderStatsSelect
    c = c.replace(
        '            renderStatsSelect() {\n'
        "                const sel = document.getElementById('statsPerson');\n"
        '                if (!sel) return;\n'
        "                const current = sel.value;\n"
        '                sel.innerHTML = \'<option value="-1">全员</option>\';\n'
        '                const staffList = this.getStaffList();\n'
        '                this.defaultStaff.forEach((name, i) => {\n'
        "                    const opt = document.createElement('option');\n"
        '                    opt.value = i;\n'
        '                    opt.textContent = staffList[i];\n'
        '                    sel.appendChild(opt);\n'
        '                });\n'
        "                sel.value = current;\n"
        '            },',
        '            renderStatsSelect() {\n'
        "                const sel = document.getElementById('statsPerson');\n"
        '                if (!sel) return;\n'
        "                const current = sel.value;\n"
        '                sel.innerHTML = \'<option value="-1">全员</option>\';\n'
        '                const staffList = this.getStaffList();\n'
        '                this.defaultStaff.forEach((name, i) => {\n'
        "                    const opt = document.createElement('option');\n"
        '                    opt.value = i;\n'
        '                    opt.textContent = staffList[i];\n'
        '                    sel.appendChild(opt);\n'
        '                });\n'
        "                sel.value = current;\n"
        '            },\n'
        '            renderTemplatePersonSelect() {\n'
        "                const sel = document.getElementById('templatePerson');\n"
        '                if (!sel) return;\n'
        "                const current = sel.value;\n"
        '                sel.innerHTML = \'<option value="">选择人员</option>\';\n'
        '                const staffList = this.getStaffList();\n'
        '                this.defaultStaff.forEach((_, i) => {\n'
        "                    const opt = document.createElement('option');\n"
        '                    opt.value = i;\n'
        '                    opt.textContent = staffList[i];\n'
        '                    sel.appendChild(opt);\n'
        '                });\n'
        "                sel.value = current;\n"
        '            },')

    # 16. applyTemplate
    c = c.replace(
        "            applyTemplate() { const person = document.getElementById('templatePerson').value; const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (!person || !patternStr) { alert('请选择人员并输入模板'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; } const rowIndex = this.defaultStaff.indexOf(person); if (rowIndex === -1) return;",
        "            applyTemplate() { const rowIndex = parseInt(document.getElementById('templatePerson').value, 10); const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (isNaN(rowIndex)) { alert('请选择人员'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; }")

    # 17. exportExcel
    c = c.replace(
        '            exportExcel() { let csv = \'姓名,\'; for (let d = 1; d <= this.daysInMonth; d++) csv += d + \'日,\'; csv = csv.slice(0, -1) + \'\\n\'; this.defaultStaff.forEach((name, rowIndex) => { csv += name; for (let col = 1; col <= this.daysInMonth; col++) { const cell = document.getElementById(`t-${rowIndex}-${col}`); csv += \',\' + (cell?.textContent || \'\'); } csv += \'\\n\'; }); const blob = new Blob([\'\\ufeff\' + csv], { type: \'text/csv;charset=utf-8;\' }); const url = URL.createObjectURL(blob); const a = document.createElement(\'a\'); a.href = url; a.download = `排班表_${this.getMonthKey()}.csv`; a.click(); URL.revokeObjectURL(url); }',
        "            exportExcel() { let csv = '姓名,'; for (let d = 1; d <= this.daysInMonth; d++) csv += d + '日,'; csv = csv.slice(0, -1) + '\\n'; const key = this.getMonthKey(); this.defaultStaff.forEach((name, rowIndex) => { csv += name; for (let col = 1; col <= this.daysInMonth; col++) { const shift = this.scheduleData[key]?.[rowIndex]?.[col] || ''; csv += ',' + shift; } csv += '\\n'; }); const blob = new Blob(['\\ufeff' + csv], { type: 'text/csv;charset=utf-8;' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `排班表_${this.getMonthKey()}.csv`; a.click(); URL.revokeObjectURL(url); }")

    # 18. clearRange after currentWeek
    c = c.replace(
        '            currentWeek() {\n'
        '                const now = new Date();\n'
        '                this.currentYear = now.getFullYear();\n'
        '                this.currentMonth = now.getMonth() + 1;\n'
        "                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;\n"
        '                this.loadMonthData();\n'
        '            },\n'
        '            setShift(row, col, shift, skipSave) {',
        '            currentWeek() {\n'
        '                const now = new Date();\n'
        '                this.currentYear = now.getFullYear();\n'
        '                this.currentMonth = now.getMonth() + 1;\n'
        "                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;\n"
        '                this.loadMonthData();\n'
        '            },\n'
        '            clearRange() {\n'
        "                document.getElementById('rangeStart').value = '';\n"
        "                document.getElementById('rangeEnd').value = '';\n"
        "                if (this.currentView === 'table') this.renderTable();\n"
        '            },\n'
        '            setShift(row, col, shift, skipSave) {')

    # 19. print media cleanup
    c = c.replace(
        '            .toolbar,\n'
        '            .stats-panel,\n'
        '            .template-section,\n'
        '            .view-toggle,\n'
        '            .week-toolbar,\n'
        '            .range-toolbar {\n'
        '                display: none !important;\n'
        '            }\n\n'
        '            .card-view,\n'
        '            .week-view,\n'
        '            .range-view {\n'
        '                display: none !important;\n'
        '            }',
        '            .toolbar,\n'
        '            .stats-panel,\n'
        '            .template-section,\n'
        '            .view-toggle,\n'
        '            .week-toolbar {\n'
        '                display: none !important;\n'
        '            }\n\n'
        '            .card-view,\n'
        '            .week-view {\n'
        '                display: none !important;\n'
        '            }')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Done', path)

modify('scheduler_v4.html')
modify('影像科月度排班系统_手机版.html')
