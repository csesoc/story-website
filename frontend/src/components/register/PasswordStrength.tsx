import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import styled, { css } from "styled-components";

interface Strength {
  strength: number
};

const selectColour = (strength: number) => {
  const colours = ["red", "orange", "yellow", "green"];
  return colours[strength - 1];
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
        <Row className="h-100">
          {range(1, 5).map(n => (
            <Col style={{ backgroundColor: strength >= n ? selectColour(strength) : "lightgray" }}></Col>
          ))}
        </Row>
      </PasswordContainer>
    </>
  );
};

export default PasswordStrength;
