import React, { useMemo, useState } from "react";
import styles from "./styles.module.css";

/* --- Inline SVG icon helper --- */
const Icon = ({ path, box = "0 0 24 24", size = 22, label }) => (
  <svg
    className={styles.iconSvg}
    viewBox={box}
    width={size}
    height={size}
    aria-hidden={label ? undefined : true}
    role={label ? "img" : "presentation"}
  >
    {label ? <title>{label}</title> : null}
    <path d={path} fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/* --- Sidebar icons (inline SVG paths) --- */
const useSidebarIcons = () => useMemo(() => ([
  { key: "menu",     path: "M3 6h18M3 12h18M3 18h18", label: "Menu" },
  { key: "grid",     path: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z", label: "Dashboard" },
  { key: "heart",    path: "M20.8 8.6a4.8 4.8 0 0 0-6.8 0L12 10.6l-2-2a4.8 4.8 0 0 0-6.8 6.8l2 2L12 22l6.8-4.6 2-2a4.8 4.8 0 0 0 0-6.8z", label: "Favourites" },
  { key: "chat",     path: "M21 15a4 4 0 0 1-4 4H8l-5 3 1.5-4A4 4 0 0 1 4 6h13a4 4 0 0 1 4 4z", label: "Messages" },
  { key: "layers",   path: "M12 2l9 5-9 5-9-5 9-5zm-7 9l7 4 7-4m-14 4l7 4 7-4", label: "Layers" },
  { key: "gift",     path: "M20 12v8H4v-8m16 0H4m16-4H4v4h16V8zm-8 0V4m0 0a2 2 0 1 1 0 4m0-4a2 2 0 1 0 0 4", label: "Gifts" },
  { key: "user",     path: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 7a4 4 0 1 0 0-8 4 4 0 0 0 0 8z", label: "Profile" },
  { key: "settings", path: "M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zm8-3.5l-1.5-.9.3-1.7-1.7-1.7-1.7.3L14.5 4h-5L8.6 6l-1.7-.3-1.7 1.7.3 1.7L4 12l1.5.9-.3 1.7 1.7 1.7 1.7-.3L9.5 20h5l.9-1.5 1.7.3 1.7-1.7-.3-1.7L20 12z", label: "Settings" },
  { key: "power",    path: "M12 2v8m6.4-4.4a8 8 0 1 1-12.8 0", label: "Power" },
]), []);

const CartPage = () => {
  const icons = useSidebarIcons();

  const initial = Array.from({ length: 6 }, (_, i) => ({
    id: i + 1,
    title: "Help Agnes go to school",
    goal: "GHS3000",
    creator: "Janet Ofori",
    amount: 0,
  }));

  const [selected, setSelected] = useState({ 1: true, 2: true }); // top two selected as in mock

  const toggleRow = (id) => setSelected((prev) => ({ ...prev, [id]: !prev[id] }));
  const selectedCount = Object.values(selected).filter(Boolean).length;

  return (
    <div className={styles.page}>
      {/* LEFT SIDEBAR */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarTop}>
          <button className={`${styles.sideIcon} ${styles.iconPrimary}`} aria-label="Menu">
            <Icon path={icons[0].path} label="Menu" />
          </button>
          <div className={styles.sideStack}>
            {icons.slice(1, 6).map((ic) => (
              <button key={ic.key} className={styles.sideIcon} aria-label={ic.label}>
                <Icon path={ic.path} />
              </button>
            ))}
          </div>
        </div>

        <div className={styles.sidebarBottom}>
          <button className={styles.sideIcon} aria-label="Profile">
            <Icon path={icons[6].path} />
          </button>
          <button className={styles.sideIcon} aria-label="Settings">
            <Icon path={icons[7].path} />
          </button>
          <button className={`${styles.sideIcon} ${styles.power}`} aria-label="Power">
            <Icon path={icons[8].path} />
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className={styles.content}>
        {/* Top bar */}
        <div className={styles.topbar}>
          <div className={styles.brand}>CauseHive<span className={styles.brandDot}>.</span></div>

          <div className={styles.searchWrap}>
            <input className={styles.search} placeholder="Search Causes" />
          </div>

          <div className={styles.userWrap}>
            <div className={styles.avatar}>
              <span className={styles.avatarBadge} />
            </div>
            <div className={styles.avatarDropdown}>
              <span className={styles.caret}>▾</span>
            </div>
          </div>
        </div>

        {/* Filters Row */}
        <div className={styles.filtersRow}>
          <div className={styles.filterPill}>
            <input className={styles.filterInput} placeholder="filter by" />
            <span className={styles.pillCaret}>▾</span>
          </div>
          <div className={styles.filterPill}>
            <input className={styles.filterInput} placeholder="" />
            <span className={styles.pillCaret}>▾</span>
          </div>
        </div>

        {/* Title */}
        <h1 className={styles.title}>Your Cart</h1>

        {/* List */}
        <div className={styles.list}>
          {initial.map((row) => (
            <div key={row.id} className={styles.row}>
              {/* left select */}
              <button
                onClick={() => toggleRow(row.id)}
                className={`${styles.tick} ${selected[row.id] ? styles.tickOn : ""}`}
                aria-pressed={!!selected[row.id]}
                aria-label={`Select ${row.title}`}
              />
              {/* card */}
              <div className={styles.card}>
                <div className={styles.cardMeta}>
                  <span className={styles.cardTitle}>{row.title}</span>
                  <span className={styles.cardDim}>Goal: {row.goal}</span>
                  <span className={styles.cardDim}>Created by: {row.creator}</span>
                </div>

                <div className={styles.amountBox}>
                  <span className={styles.amountText}>GHS {row.amount}</span>
                  <span className={styles.amountCaret}>▾</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className={styles.checkoutBar}>
          <div className={styles.selectedText}>{selectedCount} selected</div>
          <button className={styles.checkoutBtn}>Checkout</button>
        </div>
      </main>
    </div>
  );
};

export default CartPage;
