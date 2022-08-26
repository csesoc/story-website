import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

import { BACKEND_URI } from "src/config";

const Problem: React.FC<{}> = () => {
  const [times, setTimes] = useState(0);

  let { id } = useParams();

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    verifyToken();
  }, []);

  return (
    <>
      <p>This is the page for problem {id}.</p>

      <br/>

      <Container className="justify-content-center text-center">
        <p>You have clicked this button {times} times.</p>
        <Button onClick={() => setTimes(times + 1)}>Problem Page</Button>
      </Container>
    </>
  )
};

export default Problem;
