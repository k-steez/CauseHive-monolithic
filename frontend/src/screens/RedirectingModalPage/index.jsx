// index.jsx
import React, { useEffect, useState } from 'react';
import styles from './styles.module.css';

const RedirectingModalPage = () => {
  const [dots, setDots] = useState('');

  useEffect(() => {
    // Animate the ellipsis
    const interval = setInterval(() => {
      setDots(prev => {
        if (prev.length >= 3) return '';
        return prev + '.';
      });
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.modal}>
        <div className={styles.spinner}></div>
        <h1 className={styles.title}>
          Redirecting you to the payment{dots}
        </h1>
        <p className={styles.subtitle}>Please wait while we securely transfer you to our payment partner</p>
      </div>
    </div>
  );
};

export default RedirectingModalPage;