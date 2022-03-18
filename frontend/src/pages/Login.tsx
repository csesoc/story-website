import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import { BACKEND_URI } from "src/config";

const getCookieValue = (name: string) => (
  document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
);

// TODO: implement login page
const Login: React.FC<{}> = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const result = await fetch(`${BACKEND_URI}/auth/login`, {
      method: "POST",
      headers: {
        "X-CSRF-TOKEN": getCookieValue("csrf_access_token")
      },
      body: JSON.stringify({
        "email": email,
        "password": password
      })
    });

    if (!result.ok) {
			const message = `An error has occured: ${result.status}`;
      console.log("Here!");
			throw new Error(message);
		}

    navigate("/");
  };

  return (
    <>
      <Form>
        <Form.Group>
          <Form.Label>Email address</Form.Label>
          <Form.Control
            required
            type="email"
            onChange={event => setEmail(event.target.value)} />
        </Form.Group>
        <Form.Group>
          <Form.Label>Password</Form.Label>
          <Form.Control
            required
            type="password"
            onChange={event => setPassword(event.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit" onClick={() => login()}>
          Submit
        </Button>
      </Form>
    </>
  );
};

export default Login;
