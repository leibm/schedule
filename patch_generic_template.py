import re

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert generic template UI after the existing template-section content
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
            <h4>📝 按模板快速排班（团队专用）</h4>
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
            <div style="margin-top: 16px; border-top: 1px solid #e8e8e8; padding-top: 12px;">
                <h4 style="margin-bottom: 12px; font-size: 14px;">🧩 通用模板排班</h4>
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
                        <label>管理通用模板</label>
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

    if old_template_section not in content:
        print(f"[SKIP] {path}: template section not found")
        return
    content = content.replace(old_template_section, new_template_section)

    # 2. Insert generic template JS methods before applyTemplate()
    js_insert_anchor = "            applyTemplate() {"
    if js_insert_anchor not in content:
        print(f"[SKIP] {path}: applyTemplate anchor not found")
        return

    generic_js = """            genericTemplates: [],
            loadGenericTemplates() {
                const raw = localStorage.getItem('genericTemplates_v1');
                if (raw) {
                    try { this.genericTemplates = JSON.parse(raw); } catch (e) { }
                }
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

    content = content.replace(js_insert_anchor, generic_js + js_insert_anchor)

    # 3. Call loadGenericTemplates in init() after renderTemplatePersonSelect
    old_init_call = "                this.renderStatsSelect();\n                this.renderTemplatePersonSelect();"
    new_init_call = "                this.renderStatsSelect();\n                this.renderTemplatePersonSelect();\n                this.loadGenericTemplates();"
    if old_init_call in content:
        content = content.replace(old_init_call, new_init_call)
    else:
        print(f"[WARN] {path}: init call anchor not found")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")


if __name__ == '__main__':
    patch_file('scheduler_v4.html')
    patch_file('scheduler_mobile.html')
