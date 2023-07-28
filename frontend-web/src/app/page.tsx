"use client";

import { Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm, { AuthPayload } from "@/components/AuthForm";

const Login = () => {
  const handleLogin = (args: AuthPayload) => {
    console.log("Received values of form: ", args);
  };

  return (
    <div className={styles.Container}>
      <div className={styles.Block}>
        <AuthForm
          title="Login"
          submitButtonText="Log in"
          onFinish={handleLogin}
        />
        <Link href="/create-account">
          <Typography.Text>Create a account</Typography.Text>
        </Link>
      </div>
    </div>
  );
};

export default Login;
