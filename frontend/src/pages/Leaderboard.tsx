import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
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

  const [users, setUsers] = useState(defaultUsers);

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    verifyToken();
  }, []);

  return (
    <div className={styles.leaderboardPage}>
      <div>
        This is the overall leaderboard for the <span className={styles.bold}>CSESoc Unnamed Puzzle Competition 2021</span>,
        which displays the users with the highest cumulative points achieved during the contest.
      </div>
      <br />
      
      <div>
        Points awarded for completing problems - the first to solve a problem receives 100 points, followed by 99 points for
        the second solver, then 98 and so on down to 1 point for the 100th solver.
      </div>
      <br />

      {users.map((user: UserDetails) => {
        return <UserProfile position={user.position} userName={user.userName} userScore={user.userScore} userLink={user.userLink}/>
      })}
    </div>
  )
};

export default Leaderboard;
