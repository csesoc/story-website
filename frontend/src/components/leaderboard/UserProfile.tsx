import React, { useEffect, useState } from "react";
import styles from "../../App.module.css";
import { UserDetails } from "../../pages/Leaderboard";

const UserProfile = (props: UserDetails) => {
  return (
    <div className={styles.userProfile}>
        <span className={styles.profileText}>{(props.position.toString() + ")").padStart(4)}</span>
        <span className={styles.profileText}>{props.userScore.toString().padStart(4)}</span>
        {(props.userLink != "") 
          ? <a className={styles.userLinkText} href={props.userLink} target="_blank">
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
