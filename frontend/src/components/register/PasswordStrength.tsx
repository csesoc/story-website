import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import styled, { css } from "styled-components";

interface Strength {
  strength: number
};

const selectColour = (strength: number) => {
  const colours = ["red", "orange", "yellow", "greenyellow", "green"];
  return colours[strength];
};

const selectText = (strength: number) => {
  const colours = ["Very weak", "Weak", "Moderate", "Strong", "Very strong"];
  return colours[strength];
};

const range = (start: number, end: number, step: number = 1) => {
  let result = [];

  for (let i = start; i !== end; i += step) {
    result.push(i);
  }

  return result;
};

const PasswordContainer = styled(Container)`
  height: 20px;
`;

const PasswordStrength: React.FC<Strength> = ({ strength }) => {
  return (
    <>
      <PasswordContainer>
        <span style={{fontSize: 0.875+"em"}}>Password strength: <span style={{color: strength !== -1 ? selectColour(strength) : "#bdbcc1"}}>{strength !== -1 ? selectText(strength) : "N/A"}</span></span>
        <br/>
        <Row className="h-100">
          {range(0, 5).map(n => (
            <Col key={n} style={{ backgroundColor: strength >= n ? selectColour(strength) : "#bdbcc1" }}></Col>
          ))}
        </Row>
      </PasswordContainer>
    </>
  );
};

export default PasswordStrength;
