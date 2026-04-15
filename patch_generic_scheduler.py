import re

def patch_generic(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修改 title 和 h1 为通用版标识
    content = content.replace('<title>影像科月度排班系统</title>', '<title>通用排班系统</title>')
    content = content.replace('<h2>📅 影像科月度排班系统</h2>', '<h2>🧩 通用排班系统</h2>')

    # 2. 修改默认人员名单为通用示例
    old_staff = "this.defaultStaff = ['雷宝铭', '丁小涵', '徐畅', '陈钰波', '刘成伟', '刘浅予', '向锺宁'];"
    new_staff = "this.defaultStaff = ['张三', '李四', '王五'];"
    content = content.replace(old_staff, new_staff)

    # 3. 清空原有的 autoSchedule 方法，改为通用的全月自动填充提示
    old_auto = """            autoSchedule() { if (!confirm('确定要按周轮转规则自动生成本月排班吗？这会覆盖现有排班。')) return; const staff = this.defaultStaff; const weekPattern = ['白2', '留', '白3', '夜', '休', '休']; const baseTemplates = []; for (let i = 0; i < 6; i++) { const t = []; for (let d = 0; d < 7; d++) t.push(weekPattern[(i + d) % weekPattern.length]); baseTemplates.push(t); } const longBaiTemplate = ['白', '白', '白', '白', '白', '休', '休']; this.clearAll(true); let queue = null; const savedQueueState = localStorage.getItem('autoScheduleQueueState'); if (savedQueueState) { try { const state = JSON.parse(savedQueueState); const prevMonth = this.currentMonth === 1 ? 12 : this.currentMonth - 1; const prevYear = this.currentMonth === 1 ? this.currentYear - 1 : this.currentYear; if (state.year === prevYear && state.month === prevMonth) { queue = state.queue; } } catch (e) { } } if (!queue) queue = staff.map((_, i) => i); for (let day = 1; day <= this.daysInMonth; day++) { const wd = this.getWeekday(this.currentYear, this.currentMonth, day); const dayIndex = wd === 0 ? 6 : wd - 1; for (let r = 0; r < staff.length; r++) { const role = queue.indexOf(r); let shift = role === 6 ? longBaiTemplate[dayIndex] : baseTemplates[role][dayIndex]; if (wd === 0 || wd === 6) { if (shift === '白2') shift = '留'; else if (shift !== '夜') shift = '休'; } this.setShift(r, day, shift, true); } if (wd === 0) { const nextQueue = new Array(7); nextQueue[0] = queue[5]; nextQueue[1] = queue[0]; nextQueue[2] = queue[1]; nextQueue[3] = queue[6]; nextQueue[4] = queue[3]; nextQueue[5] = queue[4]; nextQueue[6] = queue[2]; for (let p = 0; p < 7; p++) queue[p] = nextQueue[p]; } } this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData)); localStorage.setItem('autoScheduleQueueState', JSON.stringify({ year: this.currentYear, month: this.currentMonth, queue })); alert('自动排班已完成！'); },"""
    new_auto = """            autoSchedule() { alert('通用版不支持自动排班，请使用下方「通用模板」功能。'); },"""
    content = content.replace(old_auto, new_auto)

    # 4. 修改 applyTemplate()：移除周末特殊转换，改为严格按模板循环
    old_apply = """            applyTemplate() { const rowIndex = parseInt(document.getElementById('templatePerson').value, 10); const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (isNaN(rowIndex)) { alert('请选择人员'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; } for (let day = 1; day < startDay; day++) { const stepsBack = startDay - day; const patternIndex = ((pattern.length - (stepsBack % pattern.length)) % pattern.length); let shift = pattern[patternIndex]; const wd = this.getWeekday(this.currentYear, this.currentMonth, day); if (wd === 0 || wd === 6) { if (shift === '白2') shift = '留'; else if (shift !== '夜') shift = '休'; } if (this.shiftTypes.includes(shift)) this.setShift(rowIndex, day, shift, true); } let normalDayCount = 0, insertWeekStartDay = 0, insertWeekEndDay = 0; for (let day = startDay; day <= this.daysInMonth; day++) { const wd = this.getWeekday(this.currentYear, this.currentMonth, day); let shift; if (wd === 5 && (insertWeekStartDay === 0 || day > insertWeekEndDay)) { const patternIndex = normalDayCount % pattern.length; if (pattern[patternIndex] === '白2') { insertWeekStartDay = day + 3; insertWeekEndDay = day + 9; } } if (insertWeekStartDay > 0 && day >= insertWeekStartDay && day <= insertWeekEndDay) { if (wd >= 1 && wd <= 5) shift = '白'; else shift = '休'; } else { const patternIndex = normalDayCount % pattern.length; shift = pattern[patternIndex]; normalDayCount++; if (wd === 0 || wd === 6) { if (shift === '白2') shift = '留'; else if (shift !== '夜') shift = '休'; } } if (this.shiftTypes.includes(shift)) this.setShift(rowIndex, day, shift, true); } this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData)); },"""
    new_apply = """            applyTemplate() { const rowIndex = parseInt(document.getElementById('templatePerson').value, 10); const startDay = parseInt(document.getElementById('templateStart').value) || 1; const patternStr = document.getElementById('templatePattern').value.trim(); if (isNaN(rowIndex)) { alert('请选择人员'); return; } const pattern = patternStr.split(/[,，]/).map(s => s.trim()).filter(s => s); if (pattern.length === 0) { alert('模板格式错误'); return; } for (let day = startDay; day <= this.daysInMonth; day++) { const shift = pattern[(day - startDay) % pattern.length]; if (this.shiftTypes.includes(shift)) this.setShift(rowIndex, day, shift, true); } this.updateStats(); localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData)); alert('模板已应用！'); },"""
    content = content.replace(old_apply, new_apply)

    # 5. 把 template-section 整个替换为通用模板 UI
    old_template_section = """        <div class="template-section">
            <h4>📝 按模板快速排班</h4>
            <div class="template-input">
                <div class="template-row">
                    <label>人员</label>
                    <select id="templatePerson">
                        <option value="">选择人员</option>
                    </select>
                </div>
                <div class="template-row">
                    <label>起始</label>
                    <input type="number" id="templateStart" min="1" max="31" value="1" style="width: 70px;">
                    <label>模板</label>
                    <input type="text" id="templatePattern" value="白2,留,白3,夜,休,休" style="flex: 2;">
                </div>
                <div class="template-row">
                    <button class="btn-primary" onclick="app.applyTemplate()" style="width: 100%;">应用模板</button>
                </div>
            </div>
        </div>"""
    new_template_section = """        <div class="template-section">
            <h4>📝 模板排班</h4>
            <div class="template-input">
                <div class="template-row">
                    <label>人员</label>
                    <select id="templatePerson">
                        <option value="">选择人员</option>
                    </select>
                </div>
                <div class="template-row">
                    <label>起始</label>
                    <input type="number" id="templateStart" min="1" max="31" value="1" style="width: 70px;">
                    <label>模板</label>
                    <input type="text" id="templatePattern" value="白,夜,休,休" style="flex: 2;">
                </div>
                <div class="template-row">
                    <button class="btn-primary" onclick="app.applyTemplate()" style="width: 100%;">应用模板</button>
                </div>
            </div>
            <div style="margin-top: 16px; border-top: 1px solid #e8e8e8; padding-top: 12px;">
                <h4 style="margin-bottom: 12px; font-size: 14px;">🧩 我的通用模板</h4>
                <div class="template-input">
                    <div class="template-row">
                        <label>人员</label>
                        <select id="genericTemplatePerson">
                            <option value="">选择人员</option>
                        </select>
                    </div>
                    <div class="template-row">
                        <label>起始</label>
                        <input type="number" id="genericTemplateStart" min="1" max="31" value="1" style="width: 60px;">
                        <label>模板</label>
                        <select id="genericTemplateSelect" style="flex: 1;">
                            <option value="">选择模板</option>
                        </select>
                    </div>
                    <div class="template-row">
                        <button class="btn-primary" onclick="app.applyGenericTemplate()" style="width: 100%;">应用通用模板</button>
                    </div>
                    <div class="template-row" style="margin-top: 8px; flex-direction: column; align-items: stretch;">
                        <label>管理模板</label>
                        <div id="genericTemplateList" style="font-size: 12px; color: #666; line-height: 1.6;"></div>
                        <div style="display: flex; gap: 6px; margin-top: 6px;">
                            <input type="text" id="newGenericTemplateName" placeholder="模板名称" style="flex: 1; min-width: 0;">
                            <input type="text" id="newGenericTemplatePattern" placeholder="班次序列，如：白,夜,休,休" style="flex: 2; min-width: 0;">
                            <button class="btn-success" onclick="app.addGenericTemplate()">+</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""
    content = content.replace(old_template_section, new_template_section)

    # 6. 在 applyTemplate() 前插入通用模板管理方法
    js_anchor = "            applyTemplate() {"
    generic_js = """            genericTemplates: [],
            loadGenericTemplates() {
                const raw = localStorage.getItem('genericTemplates_v1');
                if (raw) { try { this.genericTemplates = JSON.parse(raw); } catch (e) { } }
                if (!Array.isArray(this.genericTemplates) || this.genericTemplates.length === 0) {
                    this.genericTemplates = [{ name: '示例模板', pattern: '白,夜,休,休' }];
                }
                this.renderGenericTemplateUI();
            },
            saveGenericTemplates() {
                localStorage.setItem('genericTemplates_v1', JSON.stringify(this.genericTemplates));
                this.renderGenericTemplateUI();
            },
            renderGenericTemplateUI() {
                const sel = document.getElementById('genericTemplateSelect');
                const list = document.getElementById('genericTemplateList');
                if (sel) {
                    sel.innerHTML = '<option value="">选择模板</option>';
                    this.genericTemplates.forEach((t, i) => {
                        const opt = document.createElement('option');
                        opt.value = i;
                        opt.textContent = `${t.name} (${t.pattern})`;
                        sel.appendChild(opt);
                    });
                }
                if (list) {
                    list.innerHTML = '';
                    this.genericTemplates.forEach((t, i) => {
                        const div = document.createElement('div');
                        div.style.display = 'flex';
                        div.style.justifyContent = 'space-between';
                        div.style.alignItems = 'center';
                        div.innerHTML = `<span>• <b>${t.name}</b>：${t.pattern}</span> <button class="btn-warning" style="padding:2px 8px; font-size:12px;" onclick="app.deleteGenericTemplate(${i})">删除</button>`;
                        list.appendChild(div);
                    });
                }
                const personSel = document.getElementById('genericTemplatePerson');
                if (personSel) {
                    personSel.innerHTML = '<option value="">选择人员</option>';
                    const staffList = this.getStaffList();
                    staffList.forEach((name, i) => {
                        const opt = document.createElement('option');
                        opt.value = i;
                        opt.textContent = name;
                        personSel.appendChild(opt);
                    });
                }
            },
            addGenericTemplate() {
                const nameInput = document.getElementById('newGenericTemplateName');
                const patternInput = document.getElementById('newGenericTemplatePattern');
                const name = (nameInput.value || '').trim();
                const pattern = (patternInput.value || '').trim();
                if (!name) { alert('请输入模板名称'); return; }
                if (!pattern) { alert('请输入班次序列'); return; }
                this.genericTemplates.push({ name, pattern });
                this.saveGenericTemplates();
                nameInput.value = '';
                patternInput.value = '';
            },
            deleteGenericTemplate(index) {
                if (!confirm('确定删除该通用模板吗？')) return;
                this.genericTemplates.splice(index, 1);
                this.saveGenericTemplates();
            },
            applyGenericTemplate() {
                const rowIndex = parseInt(document.getElementById('genericTemplatePerson').value, 10);
                const startDay = parseInt(document.getElementById('genericTemplateStart').value) || 1;
                const templateIndex = document.getElementById('genericTemplateSelect').value;
                if (isNaN(rowIndex)) { alert('请选择人员'); return; }
                if (templateIndex === '') { alert('请选择模板'); return; }
                const template = this.genericTemplates[parseInt(templateIndex, 10)];
                const pattern = template.pattern.split(/[,，]/).map(s => s.trim()).filter(s => s);
                if (pattern.length === 0) { alert('模板格式错误'); return; }
                for (let day = startDay; day <= this.daysInMonth; day++) {
                    const shift = pattern[(day - startDay) % pattern.length];
                    if (this.shiftTypes.includes(shift)) {
                        this.setShift(rowIndex, day, shift, true);
                    }
                }
                this.updateStats();
                localStorage.setItem('scheduleData_v2', JSON.stringify(this.scheduleData));
                alert('通用模板已应用！');
            },
"""
    content = content.replace(js_anchor, generic_js + js_anchor)

    # 7. init() 中调用 loadGenericTemplates
    old_init = "                this.renderStatsSelect();\n                this.renderTemplatePersonSelect();"
    new_init = "                this.renderStatsSelect();\n                this.renderTemplatePersonSelect();\n                this.loadGenericTemplates();"
    content = content.replace(old_init, new_init)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch_generic('scheduler_generic.html')
    patch_generic('scheduler_generic_mobile.html')
