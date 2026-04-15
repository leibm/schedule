# 影像科排班系统

本地部署的排班管理工具，支持7人团队的周排班管理。

## 功能特点

- 📅 **周视图排班** - 清晰的周一到周日排班表
- 🎨 **可视化班次** - 不同班次用颜色区分（白班、夜班、备班、留班、休息）
- ✏️ **点击编辑** - 点击单元格快速修改班次
- 💾 **本地存储** - 数据保存在浏览器localStorage，同时支持导出JSON备份
- 📊 **导出Excel** - 一键导出CSV格式，可用Excel打开
- 🖨️ **打印友好** - 优化打印样式，可直接打印排班表
- 📈 **自动统计** - 实时显示各班次人次统计

## 班次说明

| 班次 | 说明 |
|------|------|
| 白 | 白班 |
| 白2 | 白班2 |
| 夜 | 夜班 |
| 备1 | 备班1 |
| 备2 | 备班2 |
| 留 | 留班 |
| 留备1 | 留班(备1) |
| 留备2 | 留班(备2) |
| 休 | 休息 |

## 部署方式

### 方式1：Node.js 服务器（推荐）

```bash
cd scheduler
node server.js
```

访问 http://NAS_IP:8080

### 方式2：静态文件

直接将 `index.html` 放到任何Web服务器目录即可，如：
- Nginx
- Apache
- NAS自带的Web服务

### 方式3：Docker

```bash
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html nginx
```

## 数据备份

- 点击「保存」导出JSON文件
- 数据自动保存在浏览器本地
- 换电脑或清缓存时，用「加载」恢复数据

## 修改人员名单

编辑 `index.html` 中的 `defaultStaff` 数组：

```javascript
const defaultStaff = [
    '向锺宁',
    '陈钰波',
    '刘成伟',
    '刘浅予',
    '雷宝铭',
    '丁小涵',
    '徐畅'
];
```

## 开机自启（systemd）

创建 `/etc/systemd/system/scheduler.service`：

```ini
[Unit]
Description=排班系统
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/scheduler
ExecStart=/usr/bin/node server.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用：
```bash
sudo systemctl enable scheduler
sudo systemctl start scheduler
```
