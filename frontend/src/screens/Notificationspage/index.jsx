import React, { useState } from 'react';
import styles from './styles.module.css';

const NotificationsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const notifications = [
    { id: 1, message: 'Your cause has been approved', cause: 'Giving to homeless children at Labadi' },
    { id: 2, message: 'Your cause has been approved', cause: 'Giving to homeless children at Labadi' },
    { id: 3, message: 'Your cause has been approved', cause: 'Giving to homeless children at Labadi' },
    { id: 4, message: 'Your cause has been approved', cause: 'Giving to homeless children at Labadi' },
    { id: 5, message: 'Your cause has been approved', cause: 'Giving to homeless children at Labadi' },
  ];

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className={styles.container}>
      <aside className={styles.sidebar}>
        <div className={styles.menuIcon}>☰</div>
        <button className={styles.icon}>💙</button>
        <button className={styles.icon}>💬</button>
        <button className={styles.icon}>⏳</button>
        <button className={styles.icon}>📅</button>
        <button className={styles.icon}>👤</button>
        <button className={styles.icon}>⚙️</button>
        <button className={styles.icon}>⏻</button>
      </aside>
      <main className={styles.mainContent}>
        <header className={styles.header}>
          <h1 className={styles.title}>Your notifications</h1>
          <div className={styles.searchContainer}>
            <input
              type="text"
              placeholder="Search for Causes"
              value={searchTerm}
              onChange={handleSearchChange}
              className={styles.searchInput}
            />
            <div className={styles.cartIcon}>🛒<span className={styles.cartCount}>2</span></div>
            <div className={styles.avatar}>🖤</div>
          </div>
        </header>
        <section className={styles.notificationsSection}>
          {notifications.map((notification) => (
            <div key={notification.id} className={styles.notificationItem}>
              <span className={styles.notificationDot}></span>
              <div className={styles.notificationText}>{notification.message}</div>
              <div className={styles.notificationCause}>{notification.cause}</div>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
};

export default NotificationsPage;