import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { Navigate, useNavigate } from "react-router-dom";
import styles from "../App.module.css";
import UserProfile from "../components/leaderboard/UserProfile"

import { BACKEND_URI } from "src/config";

export interface UserDetails {
  position: number;
  userName: string;
  userScore: number;
  userLink: string;
}

const Leaderboard: React.FC<{}> = () => {

  const defaultUsers: UserDetails[] = [
    {
      position: 1,
      userName: "csesoc",
      userScore: 9999,
      userLink: "https://github.com/csesoc"
    },
    {
      position: 10,
      userName: "no_github_link",
      userScore: 999,
      userLink: ""
    },
    {
      position: 100,
      userName: "a-jason-liu21",
      userScore: 99,
      userLink: "https://github.com/a-jason-liu21"
    }
  ]

  const DAYS = 7;
  const OVERALL = 0;
  const [users, setUsers] = useState(defaultUsers);
  const [day, setDay] = useState(OVERALL);

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    verifyToken();
  }, []);

  useEffect(() => {
    console.log("Doing backend query for day " + day + "!");
  }, [day]);

  return (
    <div className={styles.leaderboardPage}>
      <div>
        This is the {(day === OVERALL) ? "overall leaderboard" : ("leaderboard for day " + day)} of the <span className={styles.bold}>CSESoc Unnamed Puzzle Competition 2021</span>,
        which displays the users with the {(day === OVERALL) ? "highest cumulative points achieved during the contest" : "earliest submissions during the day"}.
      </div>
      <br />
      
      <div>
        Points awarded for completing problems - the first to solve a problem receives 100 points, followed by 99 points for
        the second solver, then 98 and so on down to 1 point for the 100th solver.
      </div>
      <br />

      <div>
        To see the leaderboard for a particular day, choose a day here: 
        {Array.from({length: DAYS},(x, i) => <span className={(day === i + 1) ? styles.daySelected : styles.dayLink} onClick = {() => setDay(i + 1)}>{i + 1}</span>)}
      </div>

      {day !== OVERALL &&
      <div>
        To see the overall leaderboard, click <span className={styles.link} onClick={() => setDay(0)}>here</span>.
      </div>}
      <br />

      {users.map((user: UserDetails) => {
        return <UserProfile position={user.position} userName={user.userName} userScore={user.userScore} userLink={user.userLink}/>
      })}
    </div>
  )
};

export default Leaderboard;
