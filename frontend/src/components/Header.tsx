import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../App.module.css";
import csesocLogo from "../csesocLogo.png";

const Header: React.FC<{}> = () => {

  const navigate = useNavigate();

  return (
    <>
      <nav className={styles.horizontalFlex}>
        <div>
          <a href="https://www.csesoc.unsw.edu.au/"> <img src={csesocLogo} alt="csesoc logo" className={styles.csesocLogo}></img> </a>
        </div>
        <div className={styles.horizontalFlex}>
          <a className={styles.navElem} href="/2022/about">[About]</a> 
          <a className={styles.navElem} href="/2022/auth/login">[Log In]</a> 
          <a className={styles.navElem} href="/2022/calendar">[Calendar]</a> 
          <a className={styles.navElem} href="/2022/leaderboard">[Leaderboard]</a> 
          <a className={styles.navElem} href="/2022/stats">[Stats]</a> 
          <div className={styles.navYear}>
            {"{"}Year={">"}<span className={styles.yearDisplay} onClick={() => navigate("/2022/")}>2022</span>{"}"}
          </div>
        </div>
      </nav>
    </>
  )
};

export default Header;
