import React, { useState } from "react";
import styles from "./styles.module.css";
import {
  Menu,
  SlidersHorizontal,
  Grid,
  Heart,
  MessageSquare,
  Layers,
  Calendar,
  User,
  Settings,
  Power,
  ShoppingCart,
  ChevronDown,
  RotateCcw,
  ChevronUp,
} from "lucide-react";

const DonationHistory = () => {
  const [filterOpen, setFilterOpen] = useState(false);
  const [filterBy, setFilterBy] = useState("Amount");

  const filters = ["Date", "Amount", "Organizer", "Category"];

  return (
    <div className={styles.app}>
      {/* LEFT SIDEBAR */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarTop}>
          <button className={styles.sideTopBtn} aria-label="Menu">
            <Menu size={18} />
          </button>
          <button className={styles.sideTopBtn} aria-label="Adjust">
            <SlidersHorizontal size={18} />
          </button>
        </div>

        <nav className={styles.sideNav} aria-label="Primary">
          <div className={styles.activeIndicator} />
          <button className={`${styles.sideBtn} ${styles.active}`} aria-label="Apps">
            <Grid size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Favorites">
            <Heart size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Messages">
            <MessageSquare size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Layers">
            <Layers size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Calendar">
            <Calendar size={20} />
          </button>
        </nav>

        <div className={styles.sideBottom}>
          <button className={styles.sideBtn} aria-label="Profile">
            <User size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Settings">
            <Settings size={20} />
          </button>
          <button className={styles.sideBtn} aria-label="Power">
            <Power size={20} />
          </button>
        </div>
      </aside>

      {/* MAIN AREA */}
      <main className={styles.main}>
        {/* TOP ROW: centered global search + cart at right */}
        <div className={styles.topRow}>
          <input
            className={styles.globalSearch}
            type="text"
            placeholder=""
            aria-label="Search"
          />
          <div className={styles.cart} aria-label="Cart">
            <ShoppingCart size={24} />
            <span className={styles.cartBadge}>2</span>
          </div>
        </div>

        {/* CONTENT CONTAINER (centred) */}
        <div className={styles.content}>
          <h1 className={styles.heading}>Donation History</h1>

          {/* FILTER BAR below heading */}
          <div className={styles.filterBar}>
            <input className={styles.inlineSearch} type="text" aria-label="Filter search" />

            <div className={styles.filterBtns}>
              <div className={styles.roundBtn} onClick={() => setFilterOpen((v) => !v)} aria-label="Choose filter">
                <ChevronDown size={16} />
                {filterOpen && (
                  <div className={styles.dropdown} role="menu">
                    {filters.map((f) => (
                      <button
                        key={f}
                        className={styles.dropdownItem}
                        onClick={() => {
                          setFilterBy(f);
                          setFilterOpen(false);
                        }}
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <button className={styles.roundBtn} aria-label="Reset">
                <RotateCcw size={16} />
              </button>

              <button className={styles.roundBtn} aria-label="Sort">
                <ChevronUp size={16} />
              </button>
            </div>
          </div>

          <div className={styles.filterHint}>Filter by: {filterBy}</div>

          {/* DONATION CARDS */}
          <div className={styles.cards}>
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className={styles.card}>
                <span className={styles.cardTitle}>Daamang Water Project</span>
                <span className={styles.cardAmount}>GHS 200.00</span>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default DonationHistory;
