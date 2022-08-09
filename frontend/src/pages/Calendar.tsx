import React, { useEffect, useState } from "react";
import { Button, Container, OverlayTrigger, Popover } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import styles from "../App.module.css";

import PuzzleBox from "../components/PuzzleBox";
import calendarImgMono from "./img/calendarImageMono.png";
import calendarImgColoured from "./img/calendarImageColoured.png";
import starMono from "./img/starMono.png";
import starColoured from "./img/starColoured.png";

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

interface buttonPos {
  left: number,
  top: number,
  radius: number,
  tooltip: "top" | "bottom" | "left" | "right"
}

// puzzle: {
//   n_parts: integer,
//   name: string,
//   dayNum: integer,
//   pixelArtLine: string
// }

const Calendar: React.FC<{}> = () => {

  let nav = useNavigate();

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

  const defaultStatus : number[] = [0, 1, 2];

  const [times, setTimes] = useState(0);
  const [showPuzzles, setShowPuzzles] = useState(defaultProblems);
  const [puzzleStatus, setPuzzleStatus] = useState(defaultStatus);

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

  const imageAspect = 16/9;
  const buttons : buttonPos[] = [
    {
      left: 10,
      top: 10,
      radius: 10,
      tooltip: "bottom"
    },
    {
      left: 30,
      top: 20,
      radius: 20,
      tooltip: "right"
    },
    { left: 50,
      top: 60,
      radius: 15,
      tooltip: "top"
    }
  ];

  return (
    <>
      <div className={styles.calendarPage}>
        <div className={styles.calendarLeft}>
          <span>Competition description placeholder</span>
        </div>
        <div className={styles.calendarRight}>
          <div className={styles.calendarImgContainer}>
            <img className={styles.calendarImgBack} src={calendarImgMono}/>
            {buttons.map((pos : buttonPos, id : number) => <OverlayTrigger
                placement = {pos.tooltip}
                overlay = {
                  <Popover className={styles.calendarPopover}>
                    <Popover.Header>Day {id + 1}</Popover.Header>
                    <Popover.Body className={styles.calendarPopoverBody}>
                      <img className={styles.calendarStar} src={(puzzleStatus[id] > 0) ? starColoured : starMono}/>
                      <img className={styles.calendarStar} src={(puzzleStatus[id] > 1) ? starColoured : starMono}/>
                    </Popover.Body>
                  </Popover>
                }
              >
              <div 
                className={styles.calendarButton} 
                style={{
                  left: pos.left + '%', 
                  top: pos.top + '%',
                  width: pos.radius + '%',
                  /* I'm setting everything to be relative to the width of the image because
                  responsiveness, but since the aspect ratio of the image is 16:9, we have this weird hack.
                  */
                height: (pos.radius * imageAspect) + '%',
                backgroundImage: "url(" + calendarImgColoured + ")",
                /* More weird stuff: we need to somehow set the background image of this button
                to be negatively offset so that it lines up perfectly with the monochrome
                background. I don't know how this works but it does, so I don't ask too many questions.
                */
                backgroundPosition: (pos.left / (100 - pos.radius) * 100) + "% " + (pos.top / (100 -pos.radius * imageAspect) * 100) + "%",
                backgroundSize: (100 / (pos.radius) * 100) + "%"
              }} 
              onClick={() => {
                nav("/2022/problem/" + (id + 1));
              }}
              />
            </OverlayTrigger>)}
          </div>
          <span>Time until next puzzle:</span>
        </div>
      </div>
    </>
  )
};

export default Calendar;
