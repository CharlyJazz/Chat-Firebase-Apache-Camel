import React, { useState } from "react";
import { Form, Input, Button, Typography } from "antd";

export interface Props {
  title: string;
  submitButtonText: string;
  onFinish: (args: CreateUserPayload) => void;
}

const AuthForm = ({ title, submitButtonText, onFinish }: Props) => {
  return (
    <>
      <Typography.Title>{title}</Typography.Title>
      <Form onFinish={onFinish}>
        <Form.Item
          name="username"
          label="Username"
          rules={[
            {
              required: true,
              message: "Please enter your username!",
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          name="password"
          label="Password"
          rules={[
            {
              required: true,
              message: "Please enter your password!",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            {submitButtonText}
          </Button>
        </Form.Item>
      </Form>
    </>
  );
};

export default AuthForm;
