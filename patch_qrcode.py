import re

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert QRCode.js CDN before </head>
    if '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>' not in content:
        content = content.replace('</head>', '    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n</head>')

    # 2. Add shareModal HTML after editModal div
    old_modal = '''    <div class="modal-overlay" id="editModal" onclick="app.closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-title" id="modalTitle">选择班次</div>
            <div class="modal-shifts" id="modalShifts"></div>
            <button class="modal-cancel" onclick="app.closeModal()">取消</button>
        </div>
    </div>'''
    new_modal = '''    <div class="modal-overlay" id="editModal" onclick="app.closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-title" id="modalTitle">选择班次</div>
            <div class="modal-shifts" id="modalShifts"></div>
            <button class="modal-cancel" onclick="app.closeModal()">取消</button>
        </div>
    </div>
    <div class="modal-overlay" id="shareModal" onclick="app.closeShareModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()" style="text-align:center;">
            <div class="modal-title">分享排班</div>
            <div id="qrcode" style="margin:12px auto; display:inline-block;"></div>
            <div style="margin-bottom:12px;">
                <button class="btn-primary" onclick="app.copyShareLink()">复制链接</button>
                <button class="modal-cancel" onclick="app.closeShareModal()">关闭</button>
            </div>
        </div>
    </div>'''
    if old_modal in content:
        content = content.replace(old_modal, new_modal)
    else:
        print(f"[WARN] {path}: editModal anchor not found")

    # 3. Replace shareSchedule and add closeShareModal / copyShareLink
    old_share = re.search(
        r"shareSchedule\(\) \{[^}]+navigator\.clipboard\.writeText\(shareUrl\)\.then\(\(\) => \{[^}]+\}\)\.catch\(\(\) => \{[^}]+\}\);\s+\},",
        content
    )
    if old_share:
        new_share = '''shareSchedule() {
                const payload = JSON.stringify(this.scheduleData);
                const encoded = btoa(encodeURIComponent(payload));
                this._shareUrl = `${window.location.origin}${window.location.pathname}#share=${encoded}`;
                const container = document.getElementById('qrcode');
                container.innerHTML = '';
                new QRCode(container, { text: this._shareUrl, width: 200, height: 200 });
                document.getElementById('shareModal').classList.add('active');
            },
            closeShareModal(e) {
                if (e && e.target !== e.currentTarget) return;
                document.getElementById('shareModal').classList.remove('active');
            },
            copyShareLink() {
                if (!this._shareUrl) return;
                navigator.clipboard.writeText(this._shareUrl).then(() => {
                    alert('链接已复制到剪贴板！');
                }).catch(() => {
                    prompt('请复制以下链接', this._shareUrl);
                });
            },'''
        content = content.replace(old_share.group(0), new_share)
    else:
        print(f"[WARN] {path}: shareSchedule block not found")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {path}")

if __name__ == '__main__':
    patch('scheduler_v4.html')
    patch('scheduler_mobile.html')
    patch('scheduler_generic.html')
    patch('scheduler_generic_mobile.html')
