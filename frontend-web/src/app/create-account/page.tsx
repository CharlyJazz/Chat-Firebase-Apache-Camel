"use client";

import { message, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm from "@/components/AuthForm";
import { useRouter } from "next/navigation";
import { fetcher } from "@/lib/swr-fetcher"; // Import the fetcher

const CreateAccount = () => {
  const [messageApi, contextHolder] = message.useMessage();
  const route = useRouter();

  const handleRegister = async (args: CreateUserPayload) => {
    try {
      const data = await fetcher<UserCreatedResponse>(
        `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/users/`,
        "POST",
        {
          username: args.username,
          password: args.password,
        }
      );

      if (data.detail) {
        messageApi.info(data.detail, 3);
      } else {
        route.replace("/");
      }
    } catch (error) {
      console.error("Error during registration:", error);
    }
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
          <Typography.Text>Already have an account?</Typography.Text>
        </Link>
      </div>
    </div>
  );
};

export default CreateAccount;
