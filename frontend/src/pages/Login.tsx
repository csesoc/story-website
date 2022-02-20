import React, { useState } from "react";
import { Form } from "react-bootstrap";

import { BACKEND_URI } from "src/config";

// TODO: implement login page
const Login: React.FC<{}> = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const result = await fetch();
  };

  return (
    <>
      <Form>
        <Form.Group>
          <Form.Label>Email address</Form.Label>
          <Form.Control
            required
            type="email"
            onChange={event => setUsername(event.target.value)} />
        </Form.Group>
      </Form>
    </>
  );
};

export default Login;
