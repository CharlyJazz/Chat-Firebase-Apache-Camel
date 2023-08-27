"use client";

import ChatContent from "@/components/ChatContent";
import { fetcher } from "@/lib/swr-fetcher";
import { Avatar, Badge, Layout, Menu, Space, Spin, Typography } from "antd";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import useSWR from "swr";

const { Sider, Content } = Layout;

const ChatPage = () => {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const route = useRouter();
  const params = useParams() as { id?: string[] };

  const {
    data: usersData,
    error: usersError,
    isLoading: usersLoading,
  } = useSWR<User[]>(
    `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/users`,
    fetcher
  );

  const users = usersData || [];

  const handleUserSelect = (user: User) => {
    route.replace(`/chat/${user.id}`);
  };

  useEffect(() => {
    if (params.id && typeof params.id[0] === "string" && users.length) {
      const currentUserId = params.id[0];
      const user = users.find((user) => user.id === parseInt(currentUserId));

      if (user) {
        setSelectedUser(user);
      }
    }
    console.log(params);
  }, [params.id, users]);

  if (usersLoading) {
    <Spin />;
  }

  return (
    <>
      <Layout style={{ minHeight: "97vh" }} hasSider>
        <Sider width={250} theme="light">
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            style={{
              height: "80vh",
              overflow: "auto",
            }}
          >
            {!usersError &&
              users.map((user) => (
                <Menu.Item key={user.id} onClick={() => handleUserSelect(user)}>
                  <Space>
                    <Badge count={1} size="small">
                      <Avatar size={"small"}>{user.username[0]}</Avatar>
                    </Badge>
                    <Typography.Text>{user.username}</Typography.Text>
                  </Space>
                </Menu.Item>
              ))}
            {usersError ? (
              <Space>
                <Typography.Text>
                  There was an error getting the users
                </Typography.Text>
              </Space>
            ) : null}
          </Menu>
        </Sider>
        <Content style={{ padding: "24px", background: "#f0f2f5" }}>
          {selectedUser ? (
            <ChatContent selectedUser={selectedUser} />
          ) : (
            <div>Please select a user from the sidebar to start chatting.</div>
          )}
        </Content>
      </Layout>
    </>
  );
};

export default ChatPage;
