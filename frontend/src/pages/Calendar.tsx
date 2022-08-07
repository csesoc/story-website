import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import styles from "../App.module.css";

import PuzzleBox from "../components/PuzzleBox";

import { BACKEND_URI } from "src/config";

export interface puzzle {
  name : string;
  dayNum : number;
  pixelArtLine : string;
  partsInfo : part[];
}

export interface part {
  partNum: number,
  description: string,
  solved: boolean,
  answer: string
}

// puzzle: {
//   n_parts: integer,
//   name: string,
//   dayNum: integer,
//   pixelArtLine: string
// }

const Calendar: React.FC<{}> = () => {
  const defaultProblems : puzzle[] = [
    {
      name: 'Manav is a very cool ice cube',
      dayNum : 1,
      pixelArtLine : '...____..._____..._______...',
      partsInfo : [],
    },
    {
      name: 'Jason is a very cool ice cube',
      dayNum : 2,
      pixelArtLine : '...____..._____..._______...',
      partsInfo : [],
    },
    {
      name: 'Hanh is a very cool ice cube',
      dayNum : 3,
      pixelArtLine : '...____..._____..._______...',
      partsInfo : [],
    },
    {
      name: 'Hanyuan is a very cool ice cube',
      dayNum : 4,
      pixelArtLine : '...____..._____..._______...',
      partsInfo : [],
    }
  ];
  const [times, setTimes] = useState(0);
  const [showPuzzles, setShowPuzzles] = useState(defaultProblems);

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    verifyToken();
  }, []);

  useEffect(() => {
    const getProblems = async () => {
      const init = {
        method: 'GET',
        headers: {
          'Content-type': 'application/json',
          Authorization: 'insertTokenhere',
        },
        body: undefined
      }
      try {
        // Note, probably need to get all questions and then delete this one manually
        // i.e. get all questions via get and then do another post request to update
        const response = await fetch(`${BACKEND_URI}/puzzle/all`, init);
        const body = await response.json();
        if (body.error) {
          alert(body.error);
        } else {
          const puzzleList = body.puzzles;
          setShowPuzzles(puzzleList);
          // fetchDelete(quizId, questionsList, body, setAlteredQuestion);
        }
      } catch (e) {
        alert(e);
      }
    }

    getProblems();
    
  }, []);

  return (
    <>
      <div className={styles.quizRightPanel}>
        {showPuzzles.map((puzzle, i) =>
        <div key={'puzzle_' + i} className={styles.puzzleBox}>
          <h2>{'Question ' + (i + 1)}</h2>
          <PuzzleBox name={puzzle.name} dayNum={puzzle.dayNum} pixelArtLine={puzzle.pixelArtLine} partsInfo={puzzle.partsInfo}/>
          <br />
        </div>)}
      </div>
    </>
  )
};

export default Calendar;
