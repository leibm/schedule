import re

DESKTOP_CSS = '''    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: #f3f4f6;
            padding: 16px;
            padding-bottom: 100px;
            color: #1f2937;
            line-height: 1.5;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #111827;
            margin-bottom: 20px;
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .view-toggle {
            display: flex;
            gap: 6px;
            margin-bottom: 20px;
            background: #f3f4f6;
            padding: 4px;
            border-radius: 12px;
        }

        .view-toggle button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            background: transparent;
            color: #6b7280;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .view-toggle button.active {
            background: #ffffff;
            color: #2563eb;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }

        .toolbar {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
            padding: 14px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .toolbar-group {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }

        .toolbar label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
        }

        input[type="month"],
        input[type="date"],
        select {
            padding: 8px 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            background: #ffffff;
            color: #374151;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        input[type="month"]:focus,
        input[type="date"]:focus,
        select:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        button {
            padding: 8px 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s ease;
            touch-action: manipulation;
        }

        button:active {
            transform: scale(0.96);
        }

        .btn-primary {
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
        }

        .btn-secondary {
            background: #ffffff;
            color: #4b5563;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .btn-success {
            background: #16a34a;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(22, 163, 74, 0.25);
        }

        .btn-warning {
            background: #f59e0b;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(245, 158, 11, 0.25);
        }

        .shift-legend {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }

        .shift-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            cursor: pointer;
            padding: 10px 6px;
            border-radius: 10px;
            transition: all 0.2s ease;
            background: #f9fafb;
            border: 1px solid transparent;
        }

        .shift-item.active {
            background: #eff6ff;
            border-color: #bfdbfe;
            box-shadow: 0 0 0 2px #2563eb;
        }

        .shift-color {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.06);
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 0 1px rgba(0,0,0,0.03);
        }

        .table-wrapper {
            overflow-x: auto;
            margin-bottom: 20px;
            display: none;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .table-wrapper.active {
            display: block;
        }

        .schedule-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 12px;
            min-width: 800px;
        }

        .schedule-table th,
        .schedule-table td {
            border: 1px solid #f3f4f6;
            padding: 7px 4px;
            text-align: center;
            min-width: 34px;
        }

        .schedule-table th {
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }

        .schedule-table th.name-header {
            min-width: 72px;
            position: sticky;
            left: 0;
            z-index: 10;
            background: #f9fafb;
            border-left: none;
        }

        .schedule-table td.name-cell {
            background: #ffffff;
            font-weight: 600;
            color: #111827;
            position: sticky;
            left: 0;
            z-index: 5;
            border-left: none;
        }

        .schedule-table td.shift-cell {
            cursor: pointer;
            transition: all 0.15s;
            height: 34px;
        }

        .schedule-table td.shift-cell:active {
            opacity: 0.7;
            transform: scale(0.96);
        }

        .schedule-table th.weekend {
            background: #fef2f2;
            color: #dc2626;
        }

        .schedule-table th.holiday {
            background: #fee2e2;
            color: #b91c1c;
        }

        .schedule-table td.weekend-bg {
            background: #fef2f2;
        }

        .card-view {
            display: none;
        }

        .card-view.active {
            display: block;
        }

        .week-view {
            display: none;
        }

        .week-view.active {
            display: block;
        }

        .week-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            padding: 12px 14px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
            gap: 8px;
        }

        .week-toolbar span {
            font-weight: 600;
            color: #111827;
            font-size: 14px;
            flex: 1;
            text-align: center;
        }

        .staff-card {
            background: #ffffff;
            border: none;
            border-radius: 16px;
            margin-bottom: 14px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        }

        .staff-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            background: #f9fafb;
            border-bottom: 1px solid #f3f4f6;
        }

        .staff-name {
            font-size: 16px;
            font-weight: 700;
            color: #111827;
        }

        .staff-summary {
            font-size: 12px;
            color: #6b7280;
            font-weight: 500;
        }

        .days-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 1px;
            background: #f3f4f6;
        }

        .day-cell {
            background: #ffffff;
            aspect-ratio: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            min-height: 54px;
            transition: all 0.15s;
            padding: 4px;
        }

        .day-cell:active {
            transform: scale(0.96);
        }

        .day-cell.weekend {
            background: #fef2f2;
        }

        .day-cell.holiday {
            background: #fef2f2;
        }

        .day-number {
            font-size: 11px;
            color: #9ca3af;
            margin-bottom: 2px;
            font-weight: 500;
        }

        .day-number.weekend-day {
            color: #dc2626;
            font-weight: 600;
        }

        .day-number.holiday-day {
            color: #b91c1c;
            font-weight: 700;
        }

        .day-number.festival-day {
            color: #2563eb;
            font-weight: 700;
        }

        .schedule-table th.festival {
            background: #eff6ff;
            color: #2563eb;
        }

        .day-cell.festival {
            background: #eff6ff;
        }

        .day-shift {
            font-size: 15px;
            font-weight: 700;
            min-height: 20px;
        }

        .stats-panel {
            margin-top: 20px;
            padding: 16px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .stats-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 12px;
        }

        .stats-header-bar h3 {
            font-size: 15px;
            font-weight: 700;
            color: #111827;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 10px;
        }

        .stat-card {
            background: #ffffff;
            padding: 12px 6px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #f3f4f6;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .stat-label {
            font-size: 11px;
            color: #6b7280;
            font-weight: 500;
        }

        .stat-value {
            font-size: 17px;
            font-weight: 700;
            color: #111827;
            margin-top: 2px;
        }

        .template-section {
            margin: 20px 0;
            padding: 16px;
            background: #eff6ff;
            border-radius: 12px;
            border: 1px solid #dbeafe;
        }

        .template-section h4 {
            margin-bottom: 14px;
            color: #1d4ed8;
            font-size: 15px;
            font-weight: 700;
        }

        .settings-section {
            margin: 20px 0;
            padding: 16px;
            background: #f0fdf4;
            border-radius: 12px;
            border: 1px solid #dcfce7;
        }

        .settings-section h4 {
            margin: 0;
            color: #15803d;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
        }

        .settings-body {
            margin-top: 14px;
        }

        .settings-row {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 12px;
        }

        .settings-row label {
            font-size: 13px;
            color: #374151;
            font-weight: 500;
        }

        .settings-row textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            resize: vertical;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        .settings-row textarea:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .template-input {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .template-row {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .template-input label {
            font-size: 13px;
            min-width: 50px;
            color: #374151;
            font-weight: 500;
        }

        .template-input input,
        .template-input select {
            flex: 1;
            min-width: 80px;
            padding: 8px 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            background: #ffffff;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        .template-input input:focus,
        .template-input select:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .reorder-btns {
            display: flex;
            gap: 4px;
        }

        .reorder-btns button {
            padding: 4px 8px;
            font-size: 12px;
        }

        .name-cell[draggable="true"] {
            cursor: grab;
        }

        .name-cell.dragging {
            opacity: 0.5;
        }

        .name-cell.drag-over {
            background: #eff6ff;
            outline: 2px dashed #2563eb;
            outline-offset: -2px;
        }

        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(17, 24, 39, 0.55);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 200;
            padding: 20px;
            backdrop-filter: blur(2px);
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-content {
            background: #ffffff;
            border-radius: 20px;
            padding: 22px;
            width: 100%;
            max-width: 340px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .modal-title {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 18px;
            text-align: center;
            color: #111827;
        }

        .modal-shifts {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 18px;
        }

        .modal-shift {
            padding: 14px;
            border-radius: 12px;
            text-align: center;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            transition: transform 0.1s;
        }

        .modal-shift:active {
            transform: scale(0.96);
        }

        .modal-cancel {
            width: 100%;
            padding: 12px;
            background: #f3f4f6;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 500;
            color: #4b5563;
            transition: background 0.15s;
        }

        .modal-cancel:hover {
            background: #e5e7eb;
        }

        @media (min-width: 768px) {
            body {
                padding: 24px;
                padding-bottom: 24px;
            }

            .container {
                padding: 28px;
            }

            h1 {
                font-size: 26px;
            }

            .shift-legend {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }

            .shift-item {
                flex-direction: row;
                padding: 8px 14px;
                gap: 8px;
            }

            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }

            .template-input {
                flex-direction: row;
                align-items: center;
            }
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
                max-width: 100%;
                padding: 10px;
            }

            .toolbar,
            .stats-panel,
            .template-section,
            .view-toggle,
            .week-toolbar,
            .range-toolbar {
                display: none !important;
            }

            .table-wrapper {
                display: block !important;
                border: none;
            }

            .card-view,
            .week-view,
            .range-view {
                display: none !important;
            }

            .schedule-table {
                font-size: 10px;
            }

            .schedule-table th,
            .schedule-table td {
                padding: 4px 2px;
            }
        }
    </style>'''

MOBILE_CSS = '''    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: #f3f4f6;
            padding: 16px;
            padding-bottom: 120px;
            color: #1f2937;
            line-height: 1.5;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #111827;
            margin-bottom: 20px;
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .view-toggle {
            display: flex;
            gap: 6px;
            margin-bottom: 20px;
            background: #f3f4f6;
            padding: 4px;
            border-radius: 12px;
        }

        .view-toggle button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            background: transparent;
            color: #6b7280;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .view-toggle button.active {
            background: #ffffff;
            color: #2563eb;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }

        .toolbar {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
            padding: 14px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .toolbar-group {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }

        .toolbar label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
        }

        input[type="month"],
        input[type="date"],
        select {
            padding: 8px 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            background: #ffffff;
            color: #374151;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        input[type="month"],
        input[type="date"] {
            max-width: 130px;
        }

        input[type="month"]:focus,
        input[type="date"]:focus,
        select:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        button {
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            touch-action: manipulation;
        }

        button:active {
            transform: scale(0.96);
        }

        .btn-primary {
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
        }

        .btn-secondary {
            background: #ffffff;
            color: #4b5563;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .btn-success {
            background: #16a34a;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(22, 163, 74, 0.25);
        }

        .btn-warning {
            background: #f59e0b;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(245, 158, 11, 0.25);
        }

        .shift-legend {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }

        .shift-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            cursor: pointer;
            padding: 10px 6px;
            border-radius: 10px;
            transition: all 0.2s ease;
            background: #f9fafb;
            border: 1px solid transparent;
        }

        .shift-item.active {
            background: #eff6ff;
            border-color: #bfdbfe;
            box-shadow: 0 0 0 2px #2563eb;
        }

        .shift-color {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.06);
            font-size: 15px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 0 1px rgba(0,0,0,0.03);
        }

        .table-wrapper {
            overflow-x: auto;
            margin-bottom: 20px;
            display: none;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .table-wrapper.active {
            display: block;
        }

        .schedule-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 12px;
            min-width: 800px;
        }

        .schedule-table th,
        .schedule-table td {
            border: 1px solid #f3f4f6;
            padding: 7px 4px;
            text-align: center;
            min-width: 34px;
        }

        .schedule-table th {
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }

        .schedule-table th.name-header {
            min-width: 72px;
            position: sticky;
            left: 0;
            z-index: 10;
            background: #f9fafb;
            border-left: none;
        }

        .schedule-table td.name-cell {
            background: #ffffff;
            font-weight: 600;
            color: #111827;
            position: sticky;
            left: 0;
            z-index: 5;
            border-left: none;
        }

        .schedule-table td.shift-cell {
            cursor: pointer;
            transition: all 0.15s;
            height: 34px;
        }

        .schedule-table td.shift-cell:active {
            opacity: 0.7;
            transform: scale(0.96);
        }

        .schedule-table th.weekend {
            background: #fef2f2;
            color: #dc2626;
        }

        .schedule-table th.holiday {
            background: #fee2e2;
            color: #b91c1c;
        }

        .schedule-table td.weekend-bg {
            background: #fef2f2;
        }

        .card-view {
            display: none;
        }

        .card-view.active {
            display: block;
        }

        .week-view {
            display: none;
        }

        .week-view.active {
            display: block;
        }

        .week-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            padding: 12px 14px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
            gap: 8px;
        }

        .week-toolbar span {
            font-weight: 600;
            color: #111827;
            font-size: 14px;
            flex: 1;
            text-align: center;
        }

        .staff-card {
            background: #ffffff;
            border: none;
            border-radius: 16px;
            margin-bottom: 14px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        }

        .staff-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            background: #f9fafb;
            border-bottom: 1px solid #f3f4f6;
        }

        .staff-name {
            font-size: 16px;
            font-weight: 700;
            color: #111827;
        }

        .staff-summary {
            font-size: 12px;
            color: #6b7280;
            font-weight: 500;
        }

        .days-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 1px;
            background: #f3f4f6;
        }

        .day-cell {
            background: #ffffff;
            aspect-ratio: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            min-height: 58px;
            transition: all 0.15s;
            padding: 6px;
        }

        .day-cell:active {
            transform: scale(0.96);
        }

        .day-cell.weekend {
            background: #fef2f2;
        }

        .day-cell.holiday {
            background: #fef2f2;
        }

        .day-number {
            font-size: 11px;
            color: #9ca3af;
            margin-bottom: 2px;
            font-weight: 500;
        }

        .day-number.weekend-day {
            color: #dc2626;
            font-weight: 600;
        }

        .day-number.holiday-day {
            color: #b91c1c;
            font-weight: 700;
        }

        .day-number.festival-day {
            color: #2563eb;
            font-weight: 700;
        }

        .schedule-table th.festival {
            background: #eff6ff;
            color: #2563eb;
        }

        .day-cell.festival {
            background: #eff6ff;
        }

        .day-shift {
            font-size: 16px;
            font-weight: 700;
            min-height: 20px;
        }

        .stats-panel {
            margin-top: 20px;
            padding: 16px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #f3f4f6;
        }

        .stats-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 12px;
        }

        .stats-header-bar h3 {
            font-size: 15px;
            font-weight: 700;
            color: #111827;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }

        .stat-card {
            background: #ffffff;
            padding: 12px 6px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #f3f4f6;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .stat-label {
            font-size: 11px;
            color: #6b7280;
            font-weight: 500;
        }

        .stat-value {
            font-size: 17px;
            font-weight: 700;
            color: #111827;
            margin-top: 2px;
        }

        .template-section {
            margin: 20px 0;
            padding: 16px;
            background: #eff6ff;
            border-radius: 12px;
            border: 1px solid #dbeafe;
        }

        .template-section h4 {
            margin-bottom: 14px;
            color: #1d4ed8;
            font-size: 15px;
            font-weight: 700;
        }

        .settings-section {
            margin: 20px 0;
            padding: 16px;
            background: #f0fdf4;
            border-radius: 12px;
            border: 1px solid #dcfce7;
        }

        .settings-section h4 {
            margin: 0;
            color: #15803d;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
        }

        .settings-body {
            margin-top: 14px;
        }

        .settings-row {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 12px;
        }

        .settings-row label {
            font-size: 13px;
            color: #374151;
            font-weight: 500;
        }

        .settings-row textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            resize: vertical;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        .settings-row textarea:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .template-input {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .template-row {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }

        .template-input label {
            font-size: 13px;
            min-width: 50px;
            color: #374151;
            font-weight: 500;
        }

        .template-input input,
        .template-input select {
            flex: 1;
            min-width: 0;
            padding: 10px 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 15px;
            background: #ffffff;
            outline: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }

        .template-input input:focus,
        .template-input select:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .name-cell[draggable="true"] {
            cursor: grab;
        }

        .name-cell.dragging {
            opacity: 0.5;
        }

        .name-cell.drag-over {
            background: #eff6ff;
            outline: 2px dashed #2563eb;
            outline-offset: -2px;
        }

        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(17, 24, 39, 0.55);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 200;
            padding: 20px;
            backdrop-filter: blur(2px);
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-content {
            background: #ffffff;
            border-radius: 20px;
            padding: 22px;
            width: 100%;
            max-width: 340px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .modal-title {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 18px;
            text-align: center;
            color: #111827;
        }

        .modal-shifts {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 18px;
        }

        .modal-shift {
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            transition: transform 0.1s;
        }

        .modal-shift:active {
            transform: scale(0.96);
        }

        .modal-cancel {
            width: 100%;
            padding: 14px;
            background: #f3f4f6;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 500;
            color: #4b5563;
            transition: background 0.15s;
        }

        .modal-cancel:hover {
            background: #e5e7eb;
        }

        @media (min-width: 768px) {
            body {
                padding: 24px;
                padding-bottom: 24px;
            }

            .container {
                padding: 28px;
            }

            h1 {
                font-size: 26px;
            }

            .shift-legend {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }

            .shift-item {
                flex-direction: row;
                padding: 8px 14px;
                gap: 8px;
            }

            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }

            .template-input {
                flex-direction: row;
                align-items: center;
            }
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
                max-width: 100%;
                padding: 10px;
            }

            .toolbar,
            .stats-panel,
            .template-section,
            .view-toggle,
            .week-toolbar,
            .range-toolbar {
                display: none !important;
            }

            .table-wrapper {
                display: block !important;
                border: none;
            }

            .card-view,
            .week-view,
            .range-view {
                display: none !important;
            }

            .schedule-table {
                font-size: 10px;
            }

            .schedule-table th,
            .schedule-table td {
                padding: 4px 2px;
            }
        }
    </style>'''

def replace_style(path, new_css):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r'<style>.*?</style>', new_css, content, count=1, flags=re.DOTALL)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Updated {path}')

replace_style('scheduler_v4.html', DESKTOP_CSS)
replace_style('scheduler_generic.html', DESKTOP_CSS)
replace_style('scheduler_mobile.html', MOBILE_CSS)
replace_style('scheduler_generic_mobile.html', MOBILE_CSS)
