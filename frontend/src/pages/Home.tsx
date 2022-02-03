import React, { useState } from "react";
import { Button, Container } from "react-bootstrap";

const Home: React.FC<{}> = () => {
  const [times, setTimes] = useState(0);

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
