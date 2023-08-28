"use client";

import { Alert, Divider, message, Spin, Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import useCreateUser from "@/api/hooks/useCreateUser"; // Import the useCreateUser hook
import AuthForm from "@/components/AuthForm"; // Make sure to import the CreateUserPayload type
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const CreateAccount = () => {
  const [messageApi, contextHolder] = message.useMessage();
  const route = useRouter();

  const {
    createAccount,
    errorCreatingAccount,
    accountCreationLoading,
    userCreated,
  } = useCreateUser(); // Use the hook here

  const handleRegister = async (args: CreateUserPayload) => {
    createAccount({
      username: args.username,
      password: args.password,
    });
  };

  useEffect(() => {
    if (!errorCreatingAccount && userCreated) {
      messageApi.info("Account created successfully!", 3);
      route.replace("/");
    }
  }, [errorCreatingAccount]);

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

        {accountCreationLoading && (
          <>
            <Divider />
            <Spin />
          </>
        )}
        {errorCreatingAccount && (
          <>
            <Divider />
            <Alert
              message="Error"
              description={errorCreatingAccount}
              type="error"
            />
          </>
        )}
      </div>
    </div>
  );
};

export default CreateAccount;
