"use client";

import { Typography } from "antd";
import Link from "next/link";
import styles from "./page.module.css";

import AuthForm, { AuthPayload } from "@/components/AuthForm";

const CreateAccount = () => {
  const handleRegister = (args: AuthPayload) => {
    console.log("Received values of form: ", args);
  };

  return (
    <div className={styles.Container}>
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
