// index.jsx
import React from 'react';
import styles from './styles.module.css';

const CausedetailPage = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.logo}>Causelive.</h1>
      </header>
      
      <main className={styles.main}>
        <h2 className={styles.title}>Details</h2>
        
        <div className={styles.campaignCard}>
          <h3 className={styles.campaignTitle}>SpringLife Donation campaign: Seeking to restore humanity.</h3>
          
          <div className={styles.infoSection}>
            <p className={styles.infoLabel}>Created by:</p>
            <p className={styles.creator}>Init dolor dot ereieum</p>
          </div>
          
          <div className={styles.infoSection}>
            <p className={styles.infoLabel}>Description:</p>
            <p className={styles.description}>
              Rewrite the narrative, save lives and people. Restore balance. Create homes and narratives.
            </p>
          </div>
          
          <div className={styles.infoSection}>
            <p className={styles.infoLabel}>Progress:</p>
            <div className={styles.progressContainer}>
              <div className={styles.progressBar}>
                <div className={styles.progressFill} style={{ width: '70%' }}></div>
              </div>
              <span className={styles.progressText}>70% reached</span>
            </div>
          </div>
          
          <div className={styles.infoSection}>
            <p className={styles.infoLabel}>Category:</p>
            <p className={styles.category}>Environment</p>
          </div>
          
          <div className={styles.actionButtons}>
            <button className={styles.donateButton}>Donate</button>
            <button className={styles.cartButton}>Add to Cart</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CausedetailPage;