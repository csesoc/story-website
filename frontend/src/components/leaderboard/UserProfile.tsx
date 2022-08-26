import React, { useEffect, useState } from "react";
import styles from "../../App.module.css";
import { UserDetails } from "../../pages/Leaderboard";

const UserProfile = (props: UserDetails) => {
  const dateStrArr = new Date(props.solveTime).toString().split(" ");
  return (
    <div className={styles.userProfile}>
        <span className={styles.profileText}>{(props.position.toString() + ")").padStart(4)}</span>
        {(props.userScore != -1)
          ? <span className={styles.profileText}>{props.userScore.toString().padStart(4)}</span>
          : <span className={styles.profileText}>{dateStrArr[1] + " " + dateStrArr[2] + "  " + dateStrArr[4]}</span>
        }
        {(props.userLink != "") 
          ? <a className={styles.link} href={props.userLink} target="_blank">
              <span className={styles.userImg}>
                  <img src={props.userLink + ".png"} height="20px"/>
              </span>
              {props.userName}
            </a> 
          : <span className={styles.userNoLinkText}>
              {props.userName}
            </span>
        }
    </div>
  )
};

export default UserProfile;
