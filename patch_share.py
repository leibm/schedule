import re

def patch(path, storage_key):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add share button after load button or save group
    old_btn = '''                <button class="btn-primary" onclick="app.loadSchedule()">📥 加载</button>
            </div>'''
    new_btn = '''                <button class="btn-primary" onclick="app.loadSchedule()">📥 加载</button>
                <button class="btn-success" onclick="app.shareSchedule()">🔗 分享</button>
            </div>'''
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
    else:
        # fallback for files without load button yet (shouldn't happen)
        old2 = '''                <button class="btn-secondary" onclick="window.print()">🖨️</button>
            </div>'''
        new2 = '''                <button class="btn-secondary" onclick="window.print()">🖨️</button>
            </div>
            <div class="toolbar-group">
                <button class="btn-success" onclick="app.shareSchedule()">🔗 分享</button>
            </div>'''
        if old2 in content:
            content = content.replace(old2, new2)
        else:
            print(f"[WARN] {path}: share button anchor not found")

    # 2. Add shareSchedule method and init hash check after loadSchedule
    load_anchor = f"""            loadSchedule() {{"""
    insert_js = f"""            shareSchedule() {{
                const payload = JSON.stringify(this.scheduleData);
                const encoded = btoa(encodeURIComponent(payload));
                const shareUrl = `${{window.location.origin}}${{window.location.pathname}}#share=${{encoded}}`;
                navigator.clipboard.writeText(shareUrl).then(() => {{
                    alert('分享链接已复制到剪贴板！');
                }}).catch(() => {{
                    prompt('请复制以下链接进行分享', shareUrl);
                }});
            }},
            """
    if load_anchor in content and "shareSchedule()" not in content:
        content = content.replace(load_anchor, insert_js + load_anchor)
    else:
        print(f"[WARN] {path}: loadSchedule anchor not found or already patched")

    # 3. In init(), after loading localStorage, check hash for shared data
    old_init = f"""                const saved = localStorage.getItem('{storage_key}');
                if (saved) {{ try {{ this.scheduleData = JSON.parse(saved); }} catch (e) {{ }} }}"""
    new_init = f"""                const saved = localStorage.getItem('{storage_key}');
                if (saved) {{ try {{ this.scheduleData = JSON.parse(saved); }} catch (e) {{ }} }}
                if (window.location.hash.startsWith('#share=')) {{
                    try {{
                        const encoded = window.location.hash.slice(7);
                        const payload = decodeURIComponent(atob(encoded));
                        const shared = JSON.parse(payload);
                        if (shared && Object.keys(shared).length) {{
                            if (confirm('检测到分享链接中的排班数据，是否加载？')) {{
                                this.scheduleData = shared;
                                localStorage.setItem('{storage_key}', JSON.stringify(this.scheduleData));
                                window.location.hash = '';
                                alert('分享排班已加载！');
                            }} else {{
                                window.location.hash = '';
                            }}
                        }}
                    }} catch (e) {{ window.location.hash = ''; }}
                }}"""
    if old_init in content:
        content = content.replace(old_init, new_init)
    else:
        print(f"[WARN] {path}: init anchor not found")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch('scheduler_v4.html', 'scheduleData_v2')
    patch('scheduler_mobile.html', 'scheduleData_v2')
    patch('scheduler_generic.html', 'scheduleData_generic_v2')
    patch('scheduler_generic_mobile.html', 'scheduleData_generic_v2')
