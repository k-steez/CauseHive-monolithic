import React from 'react';
import styles from './styles.module.css';

const CausedetailPage = () => {
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>CauseHive.</h1>
                <input type="text" placeholder="Search..." className={styles.searchInput} />
                <span className={styles.cart}>🛒2</span>
            </div>
            <div className={styles.details}>
                <h2>Details</h2>
                <p>SpringLife Donation campaign: Seeking to restore humanity.</p>
            </div>
            <div className={styles.content}>
                <div className={styles.box}></div>
                <div className={styles.box}></div>
                <div className={styles.box}></div>
            </div>
            <div className={styles.metadata}>
                <p>Created by:</p>
                <p>Init dolor dot ereieum</p>
                <p>Description:</p>
                <p>Rewrite the narrative, save lives and people. Restore balance. Create homes and narratives.</p>
                <p>Category:</p>
                <p>Environment</p>
                <div className={styles.progressContainer}>
                    <div className={styles.progressBar} style={{ width: '70%' }}></div>
                    <span>Progress: 70% reached</span>
                </div>
            </div>
            <div className={styles.buttons}>
                <button className={styles.donateBtn}>Donate</button>
                <button className={styles.cartBtn}>Add to Cart</button>
            </div>
        </div>
    );
}

export default CausedetailPage;
