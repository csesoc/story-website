import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

// Password strength checker
import { zxcvbn, zxcvbnOptions } from "@zxcvbn-ts/core";
import zxcvbnCommonPackage from "@zxcvbn-ts/language-common";
import zxcvbnEnPackage from "@zxcvbn-ts/language-en";

import { BACKEND_URI } from "src/config";
import styles from "../App.module.css";

import PasswordStrength from "src/components/register/PasswordStrength";

// Set up zxcvbn
const options = {
  dictionary: {
    ...zxcvbnCommonPackage.dictionary,
    ...zxcvbnEnPackage.dictionary,
  },
  graphs: zxcvbnCommonPackage.adjacencyGraphs,
  translations: zxcvbnEnPackage.translations,
};

zxcvbnOptions.setOptions(options);

const Register: React.FC<{}> = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [confirm, setConfirm] = useState("");

  const [strength, setStrength] = useState(-1);

  const validEmailFormat = () => {
    return /^([A-Za-z0-9_\-.])+@([A-Za-z0-9_\-.])+\.([A-Za-z]{2,})$/.test(email);
  };

  const validUserNameFormat = () => {
    return /^([A-Za-z0-9-]){3,}$/.test(username);
  }

  const canSubmit = () => {
    return validEmailFormat() && validUserNameFormat() && strength >= 3 && password === confirm;
  };

  const updatePassword = (value: string) => {
    setPassword(value);
    setStrength(zxcvbn(value).score);
  }

  const register = async () => {
    const result = await fetch(`${BACKEND_URI}/auth/register`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "email": email,
        "username": username,
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
    <div className={styles.authPage}>
      <Form>
        <Form.Group>
          <Form.Label>Email address</Form.Label>
          <Form.Control
            required
            type="email"
            onChange={event => setEmail(event.target.value)} />
          <Form.Text className="text-danger" hidden={email === "" || validEmailFormat()}>
            Invalid email
          </Form.Text>
        </Form.Group>
        <Form.Group>
          <Form.Label>Username</Form.Label>
          <Form.Control
            required
            type="text"
            onChange={event => setUsername(event.target.value)} />
          <Form.Text className="text-danger" hidden={username === "" || validUserNameFormat()}>
            Username must be at least 3 characters and contain only alphanumerics and dashes 
          </Form.Text>
        </Form.Group>
        <Form.Group>
          <Form.Label>Password</Form.Label>
          <Form.Control
            required
            type="password"
            onChange={event => updatePassword(event.target.value)} />
          <PasswordStrength strength={(password === "") ? -1 : strength} />
          <br/>
          <Form.Text className="text-danger">
            {(password === "" || strength >= 3) ? " " : "Password too weak"} 
          </Form.Text>
        </Form.Group>
        <Form.Group>
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            required
            type="password"
            onChange={event => setConfirm(event.target.value)} />
          <Form.Text className="text-danger" hidden={confirm === "" || password === confirm}>
            Passwords do not match
          </Form.Text>
        </Form.Group>
        <br/>
        <Form.Group>
          <Button
            variant="primary"
            onClick={() => register()}
            disabled={!canSubmit()}>
            Submit
          </Button>
          <Button
            variant="link"
            type="button"
            onClick={() => navigate("/2022/auth/login")}>
            Return to login
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
};

export default Register;
