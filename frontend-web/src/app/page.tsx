"use client";

import { message, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm, { AuthPayload } from "@/components/AuthForm";
import { useRouter } from "next/navigation";

const Login = () => {
  const [messageApi, contextHolder] = message.useMessage();
  const route = useRouter();

  const handleLogin = (args: AuthPayload) => {
    fetch(`${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: args.username,
        password: args.password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          messageApi.info("Credentials are wrong", 3);
        } else {
          localStorage.setItem(
            "USER_SESION",
            JSON.stringify({
              username: args.password,
              ...data,
            })
          );
          messageApi.info("User authenticated", 2, () => {
            route.replace("/chat");
          });
        }
      });
  };

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
          <Typography.Text>Create a account</Typography.Text>
        </Link>
      </div>
    </div>
  );
};

export default Login;
