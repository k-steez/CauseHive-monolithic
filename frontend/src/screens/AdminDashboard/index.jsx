import React from "react";
import styles from "./styles.module.css";
import avatarImg from "../../assets/Dashboard_image1.png";
import userBadgeImg from "../../assets/Dashboard_image2.png";

/* ---------- Small SVG helpers ---------- */
const Icon = ({ d, label }) => (
  <svg viewBox="0 0 24 24" width="20" height="20" role="img" aria-label={label} className={styles.iconSvg}>
    <path d={d} fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/* ---------- Sidebar items EXACTLY as requested ---------- */
const sidebarItems = [
{ key: "menu", label: "Menu", d: "M3 6h18M3 12h18M3 18h18" },
  { key: "dashboard", label: "Dashboard", d: "M3 13h8V3H3v10zm10 0h8V3h-8v10z" },
  { key: "favorites", label: "Favorites", d: "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5S5.4 2 12 2s10 2.69 10 6c0 3.78-3.4 6.86-8.55 11.54z" },
  { key: "inbox", label: "Inbox", d: "M4 4h16v12H4zM4 4l8 8 8-8" },
  { key: "product-stock", label: "Product Stock", d: "M4 4h16v16H4zM4 9h16M9 4v16" },
  { key: "file-manager", label: "File Manager", d: "M3 4h18v16H3zM3 4l6 6h12" },
  { key: "calendar", label: "Calendar", d: "M3 8h18M8 3v4M16 3v4M3 12h18v8H3z" },
  { key: "contact", label: "Contact", d: "M3 5h18v14H3zM3 5l9 7 9-7" },
  { key: "invoice", label: "Invoice", d: "M3 4h18v16H3zM3 8h18" },
  { key: "profile", label: "Profile", d: "M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 2a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7z" },
  { key: "settings", label: "Settings", d: "M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zm8-3.5l-1.5-.9.3-1.7-1.7-1.7-1.7.3L14.5 4h-5L8.6 6l-1.7-.3-1.7 1.7.3 1.7L4 12l1.5.9-.3 1.7 1.7 1.7 1.7-.3L9.5 20h5l.9-1.5 1.7.3 1.7-1.7-.3-1.7L20 12z" },
  { key: "ui-elements", label: "UI Elements", d: "M12 2l4 4H8l4-4zM12 22l4-4H8l4 4zM2 12l4 4V8l-4 4zm18 0l-4 4V8l4 4z" },
  { key: "logout", label: "Logout", d: "M16 17l5-5-5-5M21 12H9" },
];

/* ---------- Metrics chart data ---------- */
const chartPoints = [
  { x: 50, y: 180, lbl: "5k" },
  { x: 150, y: 140, lbl: "10k" },
  { x: 250, y: 160, lbl: "15k" },
  { x: 350, y: 130, lbl: "20k" }, // highest point (tooltip)
  { x: 450, y: 150, lbl: "25k" },
  { x: 550, y: 135, lbl: "30k" },
  { x: 650, y: 125, lbl: "35k" },
  { x: 750, y: 145, lbl: "40k" },
];

/* ---------- Metrics chart (inline SVG) ---------- */
const MetricsChart = () => (
  <svg viewBox="0 0 800 220" className={styles.chartSVG} role="img" aria-label="Metrics line chart">
    <defs>
      <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopOpacity="0.25" />
        <stop offset="100%" stopOpacity="0" />
      </linearGradient>
    </defs>

    {/* Horizontal grid + Y labels */}
    {[100, 80, 60, 40, 20].map((p, i) => (
      <g key={p}>
        <line x1="40" x2="760" y1={(i + 1) * 36} y2={(i + 1) * 36} className={styles.gridLine} />
        <text x="0" y={(i + 1) * 36 + 5} className={styles.yLabel}>{p}%</text>
      </g>
    ))}

    {/* Area under the line */}
    <path
      d={
        "M" +
        chartPoints.map((d) => `${d.x},${d.y}`).join(" L") +
        ` L ${chartPoints[chartPoints.length - 1].x} 200 L ${chartPoints[0].x} 200 Z`
      }
      fill="url(#areaFill)"
      className={styles.areaPath}
    />

    {/* Line */}
    <polyline
      points={chartPoints.map((d) => `${d.x},${d.y}`).join(" ")}
      className={styles.linePath}
      fill="none"
    />

    {/* Points */}
    {chartPoints.map((d, i) => (
      <circle key={i} cx={d.x} cy={d.y} r="4" className={styles.dataPoint} />
    ))}

    {/* Tooltip at the highest point (index 3) */}
    <g transform={`translate(${chartPoints[3].x}, ${chartPoints[3].y})`}>
      <rect x="-42" y="-26" width="84" height="20" rx="4" className={styles.tooltipBox} />
      <text x="0" y="-12" className={styles.tooltipText} textAnchor="middle">64,364.77</text>
    </g>

    {/* X labels */}
    {chartPoints.map((d, i) =>
      i % 2 === 0 ? (
        <text key={i} x={d.x} y={210} textAnchor="middle" className={styles.xLabel}>
          {d.lbl}
        </text>
      ) : null
    )}
  </svg>
);

/* ---------- Page (arrow function) ---------- */
const AdminDashboard = () => (
  <div className={styles.layoutContainer}>
    {/* Left sidebar */}
    <aside className={styles.sidebar}>
      {sidebarItems.map((item) => (
        <button key={item.key} className={styles.sideIcon} aria-label={item.label}>
          <Icon d={item.d} label={item.label} />
        </button>
      ))}
    </aside>

    {/* Right content area */}
    <div className={styles.contentArea}>
      {/* Header - centered search, visible bell, user info */}
      <header className={styles.headerBar}>
        <div className={styles.leftSlot} />
        <div className={styles.searchWrap}>
          <input className={styles.search} placeholder="Search" />
        </div>
        <div className={styles.headerRight}>
          <div className={styles.notification} aria-label="Notifications">
            {/* Bootstrap bell-fill path (MIT) */}
            <svg viewBox="0 0 16 16" className={styles.bellIcon} aria-hidden="true">
              <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z" />
            </svg>
            <span className={styles.badge}>6</span>
          </div>

          <div className={styles.user}>
            <img src={avatarImg} alt="User avatar" className={styles.avatarImg} />
            <div className={styles.userInfo}>
              <div className={styles.name}>Moni Roy</div>
              <div className={styles.role}>Admin</div>
            </div>
            <div className={styles.caret}>▾</div>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className={styles.mainContent}>
        <h1 className={styles.pageTitle}>
          Dashboard
          <img src={userBadgeImg} alt="" className={styles.titleBadge} />
        </h1>

        {/* Welcome row */}
        <section className={styles.welcomeSection}>
          <div className={styles.welcomeCard}>Welcome, Admin.</div>
          <div className={styles.highlightCard} />
        </section>

        {/* Pending Review */}
        <section className={styles.pendingSection}>
          <h2 className={styles.sectionTitle}>Donations pending review</h2>
          <div className={styles.pendingRow}>
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className={styles.pendingCard} />
            ))}
          </div>
        </section>

        {/* Metrics */}
        <section className={styles.metricsSection}>
          <div className={styles.metricsHeader}>
            <h2 className={styles.metricsTitle}>Metrics</h2>
            <select className={styles.monthSelect} aria-label="Select month">
              <option>October</option>
            </select>
          </div>
          <MetricsChart />
        </section>
      </main>
    </div>
  </div>
);

export default AdminDashboard;
