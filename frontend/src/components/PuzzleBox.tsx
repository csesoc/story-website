import React from 'react';

import PropTypes from 'prop-types';

import { useNavigate } from 'react-router-dom';
import styles from '../nav.module.css';

import {puzzle, part} from '../pages/Calendar';

function PuzzleBox (props : puzzle) {
  const navigate = useNavigate();
  console.log(props.name);
  return (
    <>
      <div className={styles.puzzleBox}>
        <span>
          {props.pixelArtLine}
        </span>

      </div>
    </>
  );
}

PuzzleBox.propTypes = {
  session: PropTypes.number,
}

export default PuzzleBox;
