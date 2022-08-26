import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import starMono from "./img/starMono.png";
import starColoured from "./img/starColoured.png";

import styles from "../App.module.css";

import { BACKEND_URI } from "src/config";

const Stats: React.FC<{}> = () => {

  const defaultSolves = [[100, 10], [200, 30], [400, 15], [100, 200], [300, 300], [20, 500], [-1, 0]]

  const [width, setWidth] = useState(window.innerWidth);
  const [solves, setSolves] = useState(defaultSolves);

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    const resize = () => {setWidth(window.innerWidth);}
    window.addEventListener('resize', resize);

    verifyToken();
    
    return () => window.removeEventListener('resize', resize);
  }, []);

  const STAR_WIDTH = 40;
  const starCount = (width / STAR_WIDTH) - 4;
  const starRep = Math.ceil(defaultSolves.reduce((prev, cur) => (prev[0] + prev[1] > cur[0] + cur[1]) ? prev : cur).reduce((prev, cur) => prev + cur, 0) / starCount);

  return (
    <div className={styles.statsPage}>
      <span>See how many competitors solved each day's problems! Gold stars represent those who solve both parts of a problem, while silver stars represent those who solve the first part.</span>
      <br/>

      <br/>
      <span>One star represents up to {starRep} people.</span>
      <br/>

      <br/>
      {solves.map((x, i) => (x[0] !== -1 && <div>
        <span>Day {i + 1}:</span>
        <span className={styles.statsGold}>{x[0].toString().padStart(4)}</span>
        <span className={styles.statsSilver}>{x[1].toString().padStart(4)}</span>
        {Array.from({length: Math.ceil(x[0] / starRep)},(x) => <img className={styles.statsMiniStar} src={starColoured}/>)}
        {Array.from({length: Math.ceil(x[1] / starRep)},(x) => <img className={styles.statsMiniStar} src={starMono}/>)}
      </div>))}
    </div>
  )
};

export default Stats;
