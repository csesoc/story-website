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
  diameter: number,
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

  const defaultStatus : number[] = [0, 1, 2, -1];
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
      diameter: 10,
      tooltip: "bottom"
    },
    {
      left: 30,
      top: 20,
      diameter: 20,
      tooltip: "right"
    },
    { left: 50,
      top: 60,
      diameter: 15,
      tooltip: "top"
    },
    {
      left: 80,
      top: 40,
      diameter: 10,
      tooltip: "left"
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
            <svg className={styles.calendarImgSvg} viewBox={"0 0 " + (imageAspect * 100) + " 100"} stroke="#FFD361">
              {buttons.map((pos : buttonPos, id : number, arr : buttonPos[]) => (id > 0) && <line
                strokeWidth={1+"px"}
                strokeDasharray="1"
                x1={arr[id - 1].left * imageAspect}
                y1={arr[id - 1].top}
                x2={arr[id].left * imageAspect}
                y2={arr[id].top}
              />)}
            </svg>
            <img className={styles.calendarImgBack} src={calendarImgMono}/>
            {buttons.map((pos : buttonPos, id : number) => <OverlayTrigger
                placement = {pos.tooltip}
                overlay = {
                  <Popover className={styles.calendarPopover}>
                    <Popover.Header>Day {id + 1}</Popover.Header>
                    <Popover.Body className={styles.calendarPopoverBody}>
                      {
                        (puzzleStatus[id] != -1) ? <>
                          <img className={styles.calendarStar} src={(puzzleStatus[id] > 0) ? starColoured : starMono}/>
                          <img className={styles.calendarStar} src={(puzzleStatus[id] > 1) ? starColoured : starMono}/>
                        </> : <span>Coming soon!</span>
                      }
                    </Popover.Body>
                  </Popover>
                }
              >
              <div 
                className={styles.calendarButton} 
                style={{
                  left: (pos.left - (pos.diameter / 2)) + '%', 
                  top: (pos.top - (pos.diameter * imageAspect / 2)) + '%',
                  width: pos.diameter + '%',
                  /* I'm setting everything to be relative to the width of the image because
                  responsiveness, but since the aspect ratio of the image is 16:9, we have this weird hack.
                  */
                  height: (pos.diameter * imageAspect) + '%',
                  backgroundImage: "url(" + ((puzzleStatus[id] == -1) ? calendarImgMono : calendarImgColoured) + ")",
                  /* More weird stuff: we need to somehow set the background image of this button
                  to be negatively offset so that it lines up perfectly with the monochrome
                  background. I don't know how this works but it does, so I don't ask too many questions.
                  */
                  backgroundPosition: ((pos.left - (pos.diameter / 2)) / (100 - pos.diameter) * 100) + "% " + 
                                      ((pos.top - (pos.diameter * imageAspect / 2)) / (100 -pos.diameter * imageAspect) * 100) + "%",
                  backgroundSize: (100 / (pos.diameter) * 100) + "%"
              }} 
              onClick={() => {
                if (puzzleStatus[id] == -1) return; nav("/2022/problem/" + (id + 1));
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
