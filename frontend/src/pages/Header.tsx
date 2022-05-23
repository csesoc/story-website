import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../App.module.css";
import csesocLogo from "../csesocLogo.png";

const Header: React.FC<{}> = () => {

  return (
    <>
      <nav className={styles.horizontalFlex}>
        <div>
          <a href="https://www.csesoc.unsw.edu.au/"> <img src={csesocLogo} alt="csesoc logo" className={styles.csesocLogo}></img> </a>
        </div>
        <div className={styles.horizontalFlex}>
          <a className={styles.navElem}>[About]</a> 
          <a className={styles.navElem}>[Log In]</a> 
          <a className={styles.navElem}>[Calendar]</a> 
          <a className={styles.navElem}>[Leaderboard]</a> 
          <a className={styles.navElem}>[Stats]</a> 
        </div>
      </nav>
    </>
  )
};

export default Header;
