import {
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

export const ganttStyle = css`
      :host {
        --g-bg: #f6f8fa;
        --g-panel: #ffffff;
        --g-border: #dbe2e8;
        --g-border-soft: #e9eef2;
        --g-text: #1f2a33;
        --g-text-muted: #5b6b79;
        --g-head-bg: #f4f7fb;
        --g-hover: #f8fbff;
        --g-shadow: 0 8px 22px rgba(42, 62, 82, 0.08);
        --g-shadow-soft: 0 2px 10px rgba(42, 62, 82, 0.06);
        --g-pending-bg: #f6c9c7;
        --g-pending-border: #d98a87;
        --g-completed-bg: #c9e8d0;
        --g-completed-border: #7ab289;
        --g-current-month: #d9eaff;
        --g-current-month-border: #84aee3;
      }

      :host {
        display: block;
        box-sizing: border-box;
        padding: 1rem;
        background: var(--g-bg);
      }

      .panel {
        max-width: 96vw;
        margin: 0 auto;
        color: var(--g-text);
      }

      h2,
      p {
        margin: 0.4rem 0;
      }

      h2 {
        font-size: 1.35rem;
        font-weight: 650;
        letter-spacing: 0.01em;
      }

      p {
        color: var(--g-text-muted);
      }

      .toolbar {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.85rem;
        align-items: end;
        margin: 1rem 0;
        padding: 1rem;
        border: 1px solid var(--g-border);
        border-radius: 14px;
        background: linear-gradient(180deg, #fbfcfe 0%, #f3f7fb 100%);
        box-shadow: var(--g-shadow-soft);
      }

      .toolbar button {
        border: 1px solid #c8d3dd;
        border-radius: 10px;
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        font-weight: 500;
        color: #2a3a47;
        transition: background 0.18s ease, border-color 0.18s ease, transform 0.14s ease;
      }

      .toolbar button {
        cursor: pointer;
        background: #ffffff;
      }

      .toolbar button:hover {
        background: var(--g-hover);
        border-color: #aebdcb;
        transform: translateY(-1px);
      }

      .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }

      .legend {
        display: flex;
        gap: 1.2rem;
        flex-wrap: wrap;
        margin-bottom: 0.9rem;
        font-size: 0.9rem;
        color: var(--g-text-muted);
      }

      .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
      }

      .square-swatch {
        width: 16px;
        height: 16px;
        border-radius: 5px;
        border: 1px solid #8ca0b2;
      }

      .chart-shell {
        border: 1px solid var(--g-border);
        border-radius: 14px;
        background: var(--g-panel);
        overflow: hidden;
        box-shadow: var(--g-shadow);
      }

      .chart-scroll {
        overflow: auto;
        height: clamp(320px, 62vh, 760px);
        background: #fcfdfe;
      }

      .month-grid {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        min-width: 720px;
      }

      .month-grid thead th {
        position: sticky;
        top: 0;
        background: var(--g-head-bg);
        z-index: 2;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-size: 0.75rem;
        color: #4c5d6b;
      }

      .month-grid th,
      .month-grid td {
        border-bottom: 1px solid var(--g-border-soft);
        padding: 0.5rem 0.45rem;
        text-align: center;
        font-size: 0.84rem;
      }

      .month-grid tbody tr:hover {
        background: #f8fbfe;
      }

      .task-col {
        text-align: left !important;
        min-width: 170px;
        max-width: 220px;
        position: sticky;
        left: 0;
        z-index: 1;
        background: #ffffff;
        border-right: 1px solid var(--g-border-soft);
        color: #243240;
        font-weight: 550;
      }

      .task-title-text {
        display: inline-block;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        vertical-align: middle;
      }

      .month-head {
        min-width: 54px;
      }

      .month-head-current {
        background: #edf5ff !important;
        color: #325b8a !important;
        box-shadow: inset 0 -2px 0 0 #7da8dc;
      }

      .month-col-current {
        background: linear-gradient(180deg, #f6faff 0%, #f2f8ff 100%);
      }

      .cell-wrap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        border: 1px solid #d5dde5;
        background: #f7f9fc;
        user-select: none;
        transition: transform 0.14s ease, box-shadow 0.18s ease, border-color 0.18s ease;
      }

      .cell-active {
        cursor: pointer;
      }

      .cell-active:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(38, 56, 73, 0.18);
      }

      .cell-pending {
        background: var(--g-pending-bg);
        border-color: var(--g-pending-border);
      }

      .cell-completed {
        background: var(--g-completed-bg);
        border-color: var(--g-completed-border);
      }

      .cell-check {
        color: #1f5a2e;
        font-size: 0.88rem;
        font-weight: 700;
        text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
      }

      .empty,
      .error {
        margin: 1rem 0;
        padding: 0.8rem 0.9rem;
        border-radius: 10px;
      }

      .empty {
        background: #f2f6fa;
        border: 1px solid #dde6ee;
        color: #496175;
      }

      .error {
        background: #fdeeee;
        border: 1px solid #f5cccc;
        color: #8a2f2f;
      }

      .tooltip {
        position: fixed;
        z-index: 20;
        pointer-events: none;
        max-width: min(360px, 88vw);
        background: rgba(255, 255, 255, 0.98);
        color: #24313f;
        border-radius: 10px;
        border: 1px solid #d2dee9;
        padding: 0.65rem 0.8rem;
        box-shadow: 0 10px 24px rgba(41, 59, 76, 0.18);
        font-size: 0.82rem;
        line-height: 1.35;
      }

      .tooltip strong {
        color: #1e3447;
      }

      .window-caption {
        color: #4f6271;
        font-size: 0.88rem;
        margin-bottom: 0.2rem;
      }

      @media (max-width: 768px) {
        :host {
          padding: 0.35rem;
        }

        h2 {
          font-size: 1.05rem;
        }

        p {
          font-size: 0.79rem;
          line-height: 1.35;
        }

        .toolbar {
          padding: 0.72rem;
          gap: 0.55rem;
          margin: 0.75rem 0;
        }

        .chart-scroll {
          height: clamp(260px, 56vh, 540px);
        }

        .button-row {
          gap: 0.35rem;
        }

        .toolbar button {
          font-size: 0.76rem;
          padding: 0.42rem 0.52rem;
          border-radius: 8px;
        }

        .legend {
          gap: 0.6rem;
          font-size: 0.77rem;
          margin-bottom: 0.55rem;
        }

        .chart-shell {
          border-radius: 10px;
        }

        .month-grid {
          min-width: 100%;
          table-layout: fixed;
        }

        .month-grid th,
        .month-grid td {
          padding: 0.33rem 0.12rem;
          font-size: 0.7rem;
        }

        .month-grid thead th {
          font-size: 0.6rem;
          letter-spacing: 0.01em;
        }

        .task-col {
          min-width: 104px;
          max-width: 116px;
          width: 108px;
          position: static;
          padding-right: 0.25rem;
        }

        .task-title-text {
          max-width: 96px;
          font-size: 0.71rem;
        }

        .month-head {
          min-width: 0;
        }

        .cell-wrap {
          width: 22px;
          height: 22px;
          border-radius: 6px;
        }

        .cell-check {
          font-size: 0.72rem;
        }

        .tooltip {
          max-width: min(320px, 92vw);
          font-size: 0.75rem;
          padding: 0.52rem 0.62rem;
        }

        .chart-scroll {
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
          max-height: 68vh;
        }
      }
    `