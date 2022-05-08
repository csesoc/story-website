import React, { useEffect, useState } from "react";
import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import { BACKEND_URI } from "src/config";

const Home: React.FC<{}> = () => {
  const [times, setTimes] = useState(0);

  useEffect(() => {
    const verifyToken = async () => {
      const result = await fetch(`${BACKEND_URI}/verify`, )
    };

    verifyToken();
  }, []);

  return (
    <>
      <Container className="justify-content-center text-center">
        <p>You have clicked this button {times} times.</p>
        <Button onClick={() => setTimes(times + 1)}>Click me!</Button>
      </Container>
    </>
  )
};

export default Home;
