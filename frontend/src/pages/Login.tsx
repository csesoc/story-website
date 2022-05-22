import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

import { BACKEND_URI } from "src/config";

const getCookieValue = (name: string) => (
  document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
);

const Login: React.FC<{}> = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const validEmailFormat = () => {
    return /^([A-Za-z0-9_\-.])+@([A-Za-z0-9_\-.])+\.([A-Za-z]{2,})$/.test(email);
  };

  const login = async () => {
    const result = await fetch(`${BACKEND_URI}/auth/login`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": getCookieValue("csrf_access_token")
      },
      body: JSON.stringify({
        "email": email,
        "password": password
      })
    });

    if (!result.ok) {
			const message = `An error has occured: ${result.status}`;
			throw new Error(message);
		} else {
      navigate("/");
    }
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
        <Button
          variant="primary"
          onClick={() => login()}
          disabled={!validEmailFormat() || password === ""}>
          Submit
        </Button>
      </Form>
    </>
  );
};

export default Login;
