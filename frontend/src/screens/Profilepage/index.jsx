import React, { useState } from "react";
import styles from "./styles.module.css";
import {
  Home,
  Grid,
  Heart,
  MessageCircle,
  Layers,
  Calendar,
  User,
  Settings,
  Power,
  Menu,
  CheckCircle,
} from "lucide-react";

// ✅ Import your local images from assets
import PaulStatamImage from "../../assets/PaulStatamImage.png"; 
import Thornimage from "../../assets/Thornimage.png"; 
import CircularFemaleImage from "../../assets/Circular_female.png"; 

const Profilepage = () => {
  const [activeTab, setActiveTab] = useState("grid");

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <div className={styles.sidebar}>
        <Menu className={styles.menuIcon} />
        <div className={styles.navTop}>
          <Home
            className={`${styles.icon} ${activeTab === "home" ? styles.active : ""}`}
            onClick={() => setActiveTab("home")}
          />
          <Grid
            className={`${styles.icon} ${activeTab === "grid" ? styles.active : ""}`}
            onClick={() => setActiveTab("grid")}
          />
          <Heart
            className={`${styles.icon} ${activeTab === "heart" ? styles.active : ""}`}
            onClick={() => setActiveTab("heart")}
          />
          <MessageCircle
            className={`${styles.icon} ${activeTab === "chat" ? styles.active : ""}`}
            onClick={() => setActiveTab("chat")}
          />
          <Layers
            className={`${styles.icon} ${activeTab === "layers" ? styles.active : ""}`}
            onClick={() => setActiveTab("layers")}
          />
          <Calendar
            className={`${styles.icon} ${activeTab === "calendar" ? styles.active : ""}`}
            onClick={() => setActiveTab("calendar")}
          />
        </div>
        <div className={styles.navBottom}>
          <User
            className={`${styles.icon} ${activeTab === "user" ? styles.active : ""}`}
            onClick={() => setActiveTab("user")}
          />
          <Settings
            className={`${styles.icon} ${activeTab === "settings" ? styles.active : ""}`}
            onClick={() => setActiveTab("settings")}
          />
          <Power
            className={`${styles.icon} ${activeTab === "power" ? styles.active : ""}`}
            onClick={() => setActiveTab("power")}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.main}>
        {/* Top Right User */}
        <div className={styles.topBar}>
          <span className={styles.username}>Paul Statham</span>
          <img
            src={PaulStatamImage}
            alt="Paul Statham"
            className={styles.topAvatar}
          />
        </div>

        {/* Banner */}
        <div className={styles.banner}>
          <div className={styles.bannerItem}> <img src={Thornimage} alt="banner 1" /> </div>
          <div className={styles.bannerItem}> <img src={Thornimage} alt="banner 2" /> </div>
          <div className={styles.bannerItem}> <img src={Thornimage} alt="banner 3" /> </div>
          <div className={styles.bannerItem}> <img src={Thornimage} alt="banner 4" /> </div>
        </div>

        {/* Profile Avatar */}
        <div className={styles.profilePicWrapper}>
          <img
            src={CircularFemaleImage}
            alt="Profile Avatar"
            className={styles.profilePic}
          />
          <CheckCircle className={styles.verifyBadge} />
        </div>

        {/* Profile Details */}
        <div className={styles.profileSection}>
          <div className={styles.profileBox}>
            <div className={styles.boxHeader}>
              <b>Name</b> John Mayer
              <span className={styles.edit}>Edit</span>
            </div>
            <p><b>Occupation</b><br />Professional Plumber</p>
            <p><b>Email</b><br />johnplumber@email.com</p>
            <p><b>Interests</b><br />I love to go fishing to see things happen in the open</p>
            <p><b>Contact</b><br />+233546091384</p>
            <p><b>Address</b><br />PaulHam Street, NY, USA</p>
          </div>

          <div className={styles.profileBox}>
            <p><b>Followers:</b></p>
            <p><b>Created Causes:</b></p>
            <p><b>Active Causes:</b></p>
          </div>
        </div>

        {/* Footer */}
        <div className={styles.footer}>2025 <b>CauseHive.</b></div>
      </div>
    </div>
  );
};

export default Profilepage;
