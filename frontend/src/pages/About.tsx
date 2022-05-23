import React from "react";

import styles from "../App.module.css";

const About: React.FC<{}> = () => {

  return (
    <>
      <div className={styles.aboutPage}>
        <div>
          Hello from the CSESoc Competitions team!
        </div>
        <br />
        <div>
          <span className={styles.bold}>Advent of Code</span> is an Advent calendar of small programming puzzles for a variety of skill sets and 
          skill levels that can be solved in any programming language you like. People use them as a speed contest,
           interview prep, company training, university coursework, practice problems, or to challenge each other.
        </div>
        <br />
        <div>
          Unlike the actual Advent of Code from which we derived our full inspiration from, this Advent is only 7 days long as is meant to be 
          completed with COMP2521 knowledge, Data Structures and Algorithms. That being said, we hope to challenge you beyond your comfort zone
          and embrace new techniques to deal with both runtime and algorithmic problems!
        </div>
        <br />
        <div>
          You don't need a computer science background to participate - just a little programming knowledge
           and some problem solving skills will get you pretty far. Nor do you need a fancy computer; every
           problem has a solution that completes in at most 15 seconds on ten-year-old hardware.
        </div>
        <br />
        <div>
          If you get stuck, try your solution against the examples given in the puzzle; you should get the same answers.
           If not, re-read the description. Did you misunderstand something? Is your program doing something you don't expect?
           After the examples work, if your answer still isn't correct, build some test cases for which you can verify the answer
           by hand and see if those work with your program. Make sure you have the entire puzzle input. 
          If you're still stuck, maybe ask a friend for help, or come back to the puzzle later. You can also ask for hints in the CSESoc Discord.
        </div>
        <br />
        <div>
          --- Credits --- <br />
          Inspiration: <br />
          <a className={styles.yearDisplay} href='https://adventofcode.com/'>Advent of Code</a><br />
          <br />
          Puzzles, Code, Design: <br />
          Competitions Team, 2022<br />
          <br />
          Beta Testing:<br />
          TBD!<br />
          <br />
          Playing: <br />
          You!<br />
        </div>
      </div>
    </>
  )
};

export default About;
