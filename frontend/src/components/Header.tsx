import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../App.module.css";
import csesocLogo from "../csesocLogo.png";

const Header: React.FC<{}> = () => {

  const navigate = useNavigate();

  const [loginState, setLoginState] = useState(false);

  const logout = () => {
    // Call logout route in backend
    navigate("/");
  }
  
  useEffect(() => {
    // Detect whether user is logged in here D:
  }, []);

  return (
    <>
      <nav className={styles.horizontalFlex}>
        <div>
          <a href="https://www.csesoc.unsw.edu.au/"> <img src={csesocLogo} alt="csesoc logo" className={styles.csesocLogo}></img> </a>
        </div>
        <div className={styles.horizontalFlex}>
          <span className={styles.navElem} onClick={() => navigate("/2022/calendar")}>[Calendar]</span> 
          <span className={styles.navElem} onClick={() => navigate("/2022/leaderboard")}>[Leaderboard]</span> 
          <span className={styles.navElem} onClick={() => navigate("/2022/stats")}>[Stats]</span> 
          <span className={styles.navElem} onClick={() => navigate("/2022/about")}>[About]</span> 
          {(loginState) 
            ? <span className={styles.navElem} onClick={logout}>[Log Out]</span>
            : <span className={styles.navElem} onClick={() => navigate("/2022/auth/login")}>[Log In / Register]</span>
          }
          <div className={styles.navYear}>
            {"{"}Year={">"}<span className={styles.yearDisplay} onClick={() => navigate("/2022/")}>2022</span>{"}"}
          </div>
        </div>
      </nav>
    </>
  )
};

export default Header;
