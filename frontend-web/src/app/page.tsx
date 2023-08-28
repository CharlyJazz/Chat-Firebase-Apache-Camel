"use client";

import { Alert, Divider, message, Spin, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import useLoginRequest from "@/api/hooks/useLoginRequest";
import AuthForm from "@/components/AuthForm"; // Make sure to import the AuthPayload type
import { useAuth } from "@/lib/Authentication";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const Login = () => {
  const [messageApi, contextHolder] = message.useMessage();

  const route = useRouter();

  const { login, authState } = useAuth();

  const { loginRequest, errorLogin, loadingLogin, authenticatedUserResponse } =
    useLoginRequest();

  const handleLogin = async (args: LoginPayload) => {
    loginRequest({
      username: args.username,
      password: args.password,
    });
  };

  useEffect(() => {
    if (!errorLogin && authenticatedUserResponse) {
      login(authenticatedUserResponse);
    }
  }, [errorLogin, authenticatedUserResponse]);

  useEffect(() => {
    if (authState.access_token) {
      messageApi.info(`Welcome ${authState.username}`, 3, () => {
        route.replace("/chat");
      });
    }
  }, [authState]);

  return (
    <div className={styles.Container}>
      {contextHolder}
      <div className={styles.Block}>
        <AuthForm
          title="Login"
          submitButtonText="Log in"
          onFinish={handleLogin}
        />
        <Link href="/create-account">
          <Typography.Text>Create an account</Typography.Text>
        </Link>
        {loadingLogin && (
          <>
            <Divider />
            <Spin />
          </>
        )}
        {errorLogin && (
          <>
            <Divider />
            <Alert message="Error" description={errorLogin} type="error" />
          </>
        )}
      </div>
    </div>
  );
};

export default Login;
