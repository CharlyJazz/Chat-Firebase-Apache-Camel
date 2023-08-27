"use client";

import { message, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm, { AuthPayload } from "@/components/AuthForm";
import { useRouter } from "next/navigation";

const CreateAccount = () => {
  const [messageApi, contextHolder] = message.useMessage();
  const route = useRouter()
  const handleRegister = (args: AuthPayload) => {
    fetch(`${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: args.username,
        password: args.password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          messageApi.info(data.detail, 3);
        } else {
          route.replace('/')
        }
      });
  };

  return (
    <div className={styles.Container}>
      {contextHolder}
      <div className={styles.Block}>
        <AuthForm
          title="Create account"
          submitButtonText="Submit"
          onFinish={handleRegister}
        />
        <Link href="/">
          <Typography.Text>Already have a account?</Typography.Text>
        </Link>
      </div>
    </div>
  );
};

export default CreateAccount;
