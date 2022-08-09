import React from 'react';

import PropTypes from 'prop-types';

import { useNavigate } from 'react-router-dom';
import styles from '../App.module.css';

import {puzzle, part} from '../pages/Calendar';

function PuzzleBox (puzzleInfo : puzzle) {
  const navigate = useNavigate();

  let numStars : number = 0;
  for (let p of puzzleInfo.partsInfo) {
    numStars += p.solved ? 1 : 0;
  }

  return (
    <>
      <div className={styles.puzzleBox}>
        <span>
          {puzzleInfo.pixelArtLine}
        </span>
        <span>
          {puzzleInfo.dayNum}
        </span>
        <span>
          {numStars} {' Stars'}
        </span>


      </div>
    </>
  );
}

PuzzleBox.propTypes = {
  session: PropTypes.number,
}

export default PuzzleBox;
