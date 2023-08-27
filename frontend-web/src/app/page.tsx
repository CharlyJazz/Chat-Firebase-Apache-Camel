"use client";

import { message, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm from "@/components/AuthForm";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/Authentication";
import { fetcher } from "@/lib/swr-fetcher";

const Login = () => {
  const [messageApi, contextHolder] = message.useMessage();

  const route = useRouter();

  const { login } = useAuth();

  const handleLogin = async (args: CreateUserPayload) => {
    try {
      const data = await fetcher<AuthenticatedUserResponse>(
        `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/login`,
        "POST",
        {
          username: args.username,
          password: args.password,
        },
        {
          "Content-Type": "application/x-www-form-urlencoded",
        }
      );

      if (data.detail) {
        messageApi.info("Credentials are wrong", 3);
      } else {
        login(data);

        messageApi.info("User authenticated", 2, () => {
          route.replace("/chat");
        });
      }
    } catch (error) {
      messageApi.info("Error during login", 3);
    }
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
