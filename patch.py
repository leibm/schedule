import sys

def modify(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Remove range button from view-toggle
    c = c.replace("<button onclick=\"app.setView('range')\">📆 范围</button>\n", "")

    # 2. Update range picker group: always visible in table view + add clear button
    c = c.replace(
        '''            <div class="toolbar-group" id="rangePickerGroup" style="display:none;">
                <label>开始</label>
                <input type="date" id="rangeStart" onchange="app.onRangeChange()">
                <label>结束</label>
                <input type="date" id="rangeEnd" onchange="app.onRangeChange()">
            </div>''',
        '''            <div class="toolbar-group" id="rangePickerGroup">
                <label>范围</label>
                <input type="date" id="rangeStart" onchange="app.onRangeChange()">
                <input type="date" id="rangeEnd" onchange="app.onRangeChange()">
                <button class="btn-secondary" onclick="app.clearRange()">整月</button>
            </div>''')

    # 3. Remove hard-coded template person options
    c = c.replace(
        '''                    <select id="templatePerson">
                        <option value="">选择人员</option>
                        <option value="向锺宁">向锺宁</option>
                        <option value="陈钰波">陈钰波</option>
                        <option value="刘成伟">刘成伟</option>
                        <option value="刘浅予">刘浅予</option>
                        <option value="雷宝铭">雷宝铭</option>
                        <option value="丁小涵">丁小涵</option>
                        <option value="徐畅">徐畅</option>
                    </select>''',
        '''                    <select id="templatePerson">
                        <option value="">选择人员</option>
                    </select>''')

    # 4. Remove #rangeView DOM block
    c = c.replace(
        '''        <div class="range-view" id="rangeView">
            <div class="range-toolbar">
                <span id="rangeLabel"></span>
            </div>
            <div class="table-wrapper" style="display:block;">
                <table class="schedule-table" id="rangeTable">
                    <thead id="rangeHead"></thead>
                    <tbody id="rangeBody"></tbody>
                </table>
            </div>
        </div>
''', '')

    # 5. Remove .range-view CSS and simplify toolbar CSS
    c = c.replace(
        '''        .range-view {
            display: none;
        }

        .range-view.active {
            display: block;
        }

        .week-toolbar,
        .range-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 10px 12px;
            background: #f8f9fa;
            border-radius: 8px;
            gap: 8px;
        }

        .week-toolbar span,
        .range-toolbar span {
            font-weight: 500;
            color: #333;
            font-size: 14px;
            flex: 1;
            text-align: center;
        }''',
        '''        .week-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 10px 12px;
            background: #f8f9fa;
            border-radius: 8px;
            gap: 8px;
        }

        .week-toolbar span {
            font-weight: 500;
            color: #333;
            font-size: 14px;
            flex: 1;
            text-align: center;
        }''')

    # 6. Remove default range values from init()
    c = c.replace(
        '''                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;
                const now = new Date();
                const fmt = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
                document.getElementById('rangeStart').value = fmt(now);
                const end = new Date(now); end.setDate(end.getDate() + 6);
                document.getElementById('rangeEnd').value = fmt(end);
                const savedOrder = localStorage.getItem('staffOrder_v2');''',
        '''                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;
                const savedOrder = localStorage.getItem('staffOrder_v2');''')

    # 7. Add renderTemplatePersonSelect in init
    c = c.replace(
        'this.renderStatsSelect();\n                this.loadMonthData();',
        'this.renderStatsSelect();\n                this.renderTemplatePersonSelect();\n                this.loadMonthData();')

    # 8. Update moveStaff/dragStaff to re-render template select
    c = c.replace(
        "localStorage.setItem('staffOrder_v2', JSON.stringify(list));\n                this.loadMonthData();",
        "localStorage.setItem('staffOrder_v2', JSON.stringify(list));\n                this.renderTemplatePersonSelect();\n                this.loadMonthData();")

    # 9. Update setView: remove range tab logic
    c = c.replace(
        '''            setView(view) {
                this.currentView = view;
                document.querySelectorAll('.view-toggle button').forEach((btn, i) => {
                    btn.classList.toggle('active', (view === 'table' && i === 0) || (view === 'card' && i === 1) || (view === 'week' && i === 2) || (view === 'range' && i === 3));
                });
                document.getElementById('tableView').classList.toggle('active', view === 'table');
                document.getElementById('cardView').classList.toggle('active', view === 'card');
                document.getElementById('weekView').classList.toggle('active', view === 'week');
                document.getElementById('rangeView').classList.toggle('active', view === 'range');
                document.getElementById('rangePickerGroup').style.display = view === 'range' ? 'flex' : 'none';
                if (view === 'week') this.renderWeekView();
                if (view === 'range') this.renderRangeView();
            },''',
        '''            setView(view) {
                this.currentView = view;
                document.querySelectorAll('.view-toggle button').forEach((btn, i) => {
                    btn.classList.toggle('active', (view === 'table' && i === 0) || (view === 'card' && i === 1) || (view === 'week' && i === 2));
                });
                document.getElementById('tableView').classList.toggle('active', view === 'table');
                document.getElementById('cardView').classList.toggle('active', view === 'card');
                document.getElementById('weekView').classList.toggle('active', view === 'week');
                if (view === 'week') this.renderWeekView();
            },''')

    # 10. loadMonthData: remove renderRangeView call
    c = c.replace(
        '''                if (this.currentView === 'week') this.renderWeekView();
                if (this.currentView === 'range') this.renderRangeView();
                const key = this.getMonthKey();''',
        '''                if (this.currentView === 'week') this.renderWeekView();
                const key = this.getMonthKey();''')

    # 11. Replace renderTable entirely + add getTableDates before it
    old_renderTable = '''            renderTable() {
                const thead = document.getElementById('tableHead'), tbody = document.getElementById('tableBody');
                const weekNames = ['日', '一', '二', '三', '四', '五', '六'];
                let headHTML = '<tr><th class="name-header">姓名</th>';
                for (let d = 1; d <= this.daysInMonth; d++) {
                    const wd = this.getWeekday(this.currentYear, this.currentMonth, d);
                    const holiday = this.isHoliday(this.currentYear, this.currentMonth, d);
                    const cls = [wd === 0 || wd === 6 ? 'weekend' : '', holiday ? 'holiday' : ''].filter(Boolean).join(' ');
                    headHTML += `<th class="${cls}">${d}<br><small>周${weekNames[wd]}${holiday ? ' ' + holiday : ''}</small></th>`;
                }
                headHTML += '</tr>';
                thead.innerHTML = headHTML;
                tbody.innerHTML = '';
                const staffList = this.getStaffList();
                this.defaultStaff.forEach((_, dataRow) => {
                    const name = staffList[dataRow];
                    const tr = document.createElement('tr');
                    const nameTd = document.createElement('td');
                    nameTd.className = 'name-cell';
                    nameTd.textContent = name;
                    this.bindDragEvents(nameTd, dataRow);
                    tr.appendChild(nameTd);
                    for (let col = 1; col <= this.daysInMonth; col++) {
                        const td = document.createElement('td');
                        td.className = 'shift-cell';
                        td.id = `t-${dataRow}-${col}`;
                        td.addEventListener('click', () => this.setShift(dataRow, col, this.currentShift));
                        tr.appendChild(td);
                    }
                    tbody.appendChild(tr);
                });
            },'''

    new_renderTable = '''            getTableDates() {
                const startVal = document.getElementById('rangeStart').value;
                const endVal = document.getElementById('rangeEnd').value;
                const dates = [];
                if (!startVal || !endVal) {
                    for (let d = 1; d <= this.daysInMonth; d++) dates.push(new Date(this.currentYear, this.currentMonth - 1, d));
                    return dates;
                }
                let start = new Date(startVal);
                let end = new Date(endVal);
                if (start > end) { [start, end] = [end, start]; }
                const diffDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));
                if (diffDays > 30) {
                    end = new Date(start); end.setDate(end.getDate() + 30);
                    const fmt = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
                    document.getElementById('rangeEnd').value = fmt(end);
                }
                for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) dates.push(new Date(d));
                return dates;
            },
            renderTable() {
                const thead = document.getElementById('tableHead'), tbody = document.getElementById('tableBody');
                const weekNames = ['日', '一', '二', '三', '四', '五', '六'];
                const dates = this.getTableDates();
                const isCurrentMonthOnly = dates.every(d => d.getFullYear() === this.currentYear && d.getMonth() + 1 === this.currentMonth);
                let headHTML = '<tr><th class="name-header">姓名</th>';
                dates.forEach(date => {
                    const d = date.getDate();
                    const wd = date.getDay();
                    const holiday = this.isHoliday(date.getFullYear(), date.getMonth() + 1, d);
                    const cls = [wd === 0 || wd === 6 ? 'weekend' : '', holiday ? 'holiday' : ''].filter(Boolean).join(' ');
                    const label = isCurrentMonthOnly ? d : `${date.getMonth() + 1}/${d}`;
                    headHTML += `<th class="${cls}">${label}<br><small>周${weekNames[wd]}${holiday ? ' ' + holiday : ''}</small></th>`;
                });
                headHTML += '</tr>';
                thead.innerHTML = headHTML;
                tbody.innerHTML = '';
                const staffList = this.getStaffList();
                this.defaultStaff.forEach((_, dataRow) => {
                    const name = staffList[dataRow];
                    const tr = document.createElement('tr');
                    const nameTd = document.createElement('td');
                    nameTd.className = 'name-cell';
                    nameTd.textContent = name;
                    this.bindDragEvents(nameTd, dataRow);
                    tr.appendChild(nameTd);
                    dates.forEach(date => {
                        const y = date.getFullYear(), m = date.getMonth() + 1, d = date.getDate();
                        const wd = date.getDay();
                        const td = document.createElement('td');
                        td.className = 'shift-cell';
                        if (wd === 0 || wd === 6) td.classList.add('weekend-bg');
                        if (isCurrentMonthOnly) {
                            td.id = `t-${dataRow}-${d}`;
                            td.addEventListener('click', () => this.setShift(dataRow, d, this.currentShift));
                        } else {
                            const key = `${y}-${String(m).padStart(2, '0')}`;
                            const shift = this.scheduleData[key]?.[dataRow]?.[d] || '';
                            td.textContent = shift;
                            td.classList.add('shift-' + (shift || 'empty'));
                            td.addEventListener('click', () => {
                                const origYear = this.currentYear, origMonth = this.currentMonth, origDays = this.daysInMonth;
                                this.currentYear = y; this.currentMonth = m; this.daysInMonth = this.getDaysInMonth(y, m);
                                this.setShift(dataRow, d, this.currentShift);
                                this.currentYear = origYear; this.currentMonth = origMonth; this.daysInMonth = origDays;
                            });
                        }
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            },'''

    c = c.replace(old_renderTable, new_renderTable)

    # 12. Update onRangeChange
    c = c.replace(
        '''            onRangeChange() {
                if (this.currentView === 'range') this.renderRangeView();
            },''',
        '''            onRangeChange() {
                if (this.currentView === 'table') this.renderTable();
            },''')

    # 13. Remove renderRangeView method
    start_idx = c.find('            renderRangeView() {')
    end_marker = '            },\n            prevWeek() {'
    end_idx = c.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        c = c[:start_idx] + '            ' + c[end_idx + len(end_marker) - len('prevWeek() {'):]

    # 14. Update setShift to redraw cross-month table
    c = c.replace(
        '''                if (!skipSave) { this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData)); }
            },
            updateSummary(row) {''',
        '''                if (!skipSave) {
                    this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData));
                    if (this.currentView === 'table') {
                        const dates = this.getTableDates();
                        const isCrossMonth = dates.some(d => d.getFullYear() !== this.currentYear || d.getMonth() + 1 !== this.currentMonth);
                        if (isCrossMonth) this.renderTable();
                    }
                }
            },
            updateSummary(row) {''')

    # 15. Add renderTemplatePersonSelect after renderStatsSelect
    c = c.replace(
        '''            renderStatsSelect() {
                const sel = document.getElementById('statsPerson');
                if (!sel) return;
                const current = sel.value;
                sel.innerHTML = '<option value="-1">全员</option>';
                const staffList = this.getStaffList();
                this.defaultStaff.forEach((name, i) => {
                    const opt = document.createElement('option');
                    opt.value = i;
                    opt.textContent = staffList[i];
                    sel.appendChild(opt);
                });
                sel.value = current;
            },''',
        '''            renderStatsSelect() {
                const sel = document.getElementById('statsPerson');
                if (!sel) return;
                const current = sel.value;
                sel.innerHTML = '<option value="-1">全员</option>';
                const staffList = this.getStaffList();
                this.defaultStaff.forEach((name, i) => {
                    const opt = document.createElement('option');
                    opt.value = i;
                    opt.textContent = staffList[i];
                    sel.appendChild(opt);
                });
                sel.value = current;
            },
            renderTemplatePersonSelect() {
                const sel = document.getElementById('templatePerson');
                if (!sel) return;
                const current = sel.value;
                sel.innerHTML = '<option value="">选择人员</option>';
                const staffList = this.getStaffList();
                this.defaultStaff.forEach((_, i) => {
                    const opt = document.createElement('option');
                    opt.value = i;
                    opt.textContent = staffList[i];
                    sel.appendChild(opt);
                });
                sel.value = current;
            },''')

    # 16. Update applyTemplate to use row index from select
    c = c.replace(
        '''            applyTemplate() { const person = document.getElementById('templatePerson').value; const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (!person || !patternStr) { alert('请选择人员并输入模板'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; } const rowIndex = this.defaultStaff.indexOf(person); if (rowIndex === -1) return;''',
        '''            applyTemplate() { const rowIndex = parseInt(document.getElementById('templatePerson').value, 10); const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (isNaN(rowIndex)) { alert('请选择人员'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; }''')

    # 17. Update exportExcel to read from scheduleData instead of DOM
    c = c.replace(
        '''            exportExcel() { let csv = '姓名,'; for (let d = 1; d <= this.daysInMonth; d++) csv += d + '日,'; csv = csv.slice(0, -1) + '\\n'; this.defaultStaff.forEach((name, rowIndex) => { csv += name; for (let col = 1; col <= this.daysInMonth; col++) { const cell = document.getElementById(`t-${rowIndex}-${col}`); csv += ',' + (cell?.textContent || ''); } csv += '\\n'; }); const blob = new Blob(['\\ufeff' + csv], { type: 'text/csv;charset=utf-8;' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `排班表_${this.getMonthKey()}.csv`; a.click(); URL.revokeObjectURL(url); }''',
        '''            exportExcel() { let csv = '姓名,'; for (let d = 1; d <= this.daysInMonth; d++) csv += d + '日,'; csv = csv.slice(0, -1) + '\\n'; const key = this.getMonthKey(); this.defaultStaff.forEach((name, rowIndex) => { csv += name; for (let col = 1; col <= this.daysInMonth; col++) { const shift = this.scheduleData[key]?.[rowIndex]?.[col] || ''; csv += ',' + shift; } csv += '\\n'; }); const blob = new Blob(['\\ufeff' + csv], { type: 'text/csv;charset=utf-8;' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `排班表_${this.getMonthKey()}.csv`; a.click(); URL.revokeObjectURL(url); }''')

    # 18. Add clearRange after currentWeek
    c = c.replace(
        '''            currentWeek() {
                const now = new Date();
                this.currentYear = now.getFullYear();
                this.currentMonth = now.getMonth() + 1;
                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;
                this.loadMonthData();
            },
            setShift(row, col, shift, skipSave) {''',
        '''            currentWeek() {
                const now = new Date();
                this.currentYear = now.getFullYear();
                this.currentMonth = now.getMonth() + 1;
                document.getElementById('monthPicker').value = `${this.currentYear}-${String(this.currentMonth).padStart(2, '0')}`;
                this.loadMonthData();
            },
            clearRange() {
                document.getElementById('rangeStart').value = '';
                document.getElementById('rangeEnd').value = '';
                if (this.currentView === 'table') this.renderTable();
            },
            setShift(row, col, shift, skipSave) {''')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Modified', path)

modify('scheduler_v4.html')
modify('影像科月度排班系统_手机版.html')
