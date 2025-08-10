import React from 'react';
import styles from './styles.module.css';

import { useNavigate } from 'react-router-dom';

// Placeholder icons as SVG components for each sidebar item
const MenuIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <rect y="4" width="24" height="2" rx="1" />
    <rect y="11" width="24" height="2" rx="1" />
    <rect y="18" width="24" height="2" rx="1" />
  </svg>
);

const DashboardIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <rect x="3" y="3" width="7" height="7" rx="1" />
    <rect x="14" y="3" width="7" height="7" rx="1" />
    <rect x="14" y="14" width="7" height="7" rx="1" />
    <rect x="3" y="14" width="7" height="7" rx="1" />
  </svg>
);

const FavoritesIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 1.01 4.5 2.09C13.09 4.01 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
  </svg>
);

const InboxIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
  </svg>
);

const OrderListsIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <rect x="3" y="4" width="18" height="2" rx="1" />
    <rect x="3" y="10" width="18" height="2" rx="1" />
    <rect x="3" y="16" width="18" height="2" rx="1" />
  </svg>
);

const CalendarIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
    <line x1="16" y1="2" x2="16" y2="6" stroke="#2f3e46" strokeWidth="2" />
    <line x1="8" y1="2" x2="8" y2="6" stroke="#2f3e46" strokeWidth="2" />
  </svg>
);

const ProfileIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <circle cx="12" cy="8" r="4" />
    <path d="M4 20c0-4 8-4 8-4s8 0 8 4v2H4v-2z" />
  </svg>
);

const SettingsIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
  </svg>
);

const LogoutIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M16 13v-2H7V8l-5 4 5 4v-3zM20 3h-8v2h8v14h-8v2h8a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z" />
  </svg>
);

const CartIcon = () => (
  <svg width="24" height="24" fill="#2f3e46" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M7 18c-1.104 0-2 .896-2 2s.896 2 2 2 2-.896 2-2-.896-2-2-2zm10 0c-1.104 0-2 .896-2 2s.896 2 2 2 2-.896 2-2-.896-2-2-2zm-12.83-2l1.72-7h11.22l1.72 7h-14.66zm15.83-9h-16l-1-4h-2v2h1l3.6 7.59-1.35 2.44c-.16.28-.25.61-.25.97 0 1.104.896 2 2 2h12v-2h-11.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49-1.74-1z"/>
  </svg>
);

const CartItem = () => (
  <div className={styles.cartItem}>
    <div className={styles.imagePlaceholder}></div>
    <div className={styles.textPlaceholder}></div>
  </div>
);

const CartPage = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Navigate user out of CartPage, e.g., to sign-in page
    navigate('/sign-in');
  };

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <button className={styles.sidebarIcon} aria-label="Menu">
          <MenuIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Dashboard">
          <DashboardIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Favorites">
          <FavoritesIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Inbox">
          <InboxIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Order Lists">
          <OrderListsIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Calendar">
          <CalendarIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Profile">
          <ProfileIcon />
        </button>
        <button className={styles.sidebarIcon} aria-label="Settings">
          <SettingsIcon />
        </button>
        <button
          className={styles.sidebarIcon}
          aria-label="Logout"
          onClick={handleLogout}
        >
          <LogoutIcon />
        </button>
      </aside>

      {/* Main content */}
      <main className={styles.mainContent}>
        {/* Header */}
        <header className={styles.header}>
          <h1 className={styles.logo}>CauseHive.</h1>
          <h2 className={styles.title}>Your Cart</h2>
          <input type="text" placeholder="Search" className={styles.searchInput} />
          <div className={styles.cartIconWrapper}>
            <CartIcon />
            <span className={styles.cartBadge}>2</span>
          </div>
        </header>

        {/* Filters */}
        <section className={styles.filters}>
          <div className={styles.filterInputWrapper}>
            <input type="text" placeholder="filter by" className={styles.filterInput} />
            <button className={styles.dropdownButton} aria-label="Filter dropdown">&#9660;</button>
          </div>
          <div className={styles.filterInputWrapper}>
            <input type="text" className={styles.filterInput} />
            <button className={styles.dropdownButtonAlt} aria-label="Filter dropdown">&#9660;</button>
          </div>
        </section>

        {/* Cart items list */}
        <section className={styles.cartList}>
          {[...Array(6)].map((_, i) => (
            <CartItem key={i} />
          ))}
        </section>

        {/* Checkout button */}
        <button className={styles.checkoutButton}>Checkout</button>
      </main>
    </div>
  );
};

export default CartPage;
