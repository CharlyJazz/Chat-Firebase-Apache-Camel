"use client";

import useSWR from "swr";
import {
  Layout,
  Menu,
  Avatar,
  List,
  Input,
  Button,
  Badge,
  Typography,
  Space,
  Row,
  Col,
  Spin,
} from "antd";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const { Sider, Content } = Layout;

interface User {
  id: number;
  username: string;
}

const fetcher = async (url: string) => {
  let storedValue = localStorage.getItem("USER_SESION");

  const requestInit: RequestInit = {};

  if (storedValue) {
    const token = JSON.parse(storedValue)?.access_token;
    if (typeof token === "string" && token.length) {
      requestInit.headers = {
        Authorization: `Bearer ${token}`,
      };
    }
  }

  const response = await fetch(url, requestInit);

  if (!response.ok) {
    const error = new Error("An error occurred while fetching the data.");
    // Attach extra info to the error object.
    error.message = await response.json();
    error.name = `Status ${response.status}`;
    throw error;
  }

  const data = await response.json();
  return data;
};

const ChatPage = () => {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [messages, setMessages] = useState<any[]>([]); // Update the message type as needed
  const [messageText, setMessageText] = useState("");

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

  const handleSendMessage = () => {
    setMessages([...messages, { sender: "You", text: messageText }]);
    setMessageText("");
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
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                flex: 1,
                height: "100%",
              }}
            >
              <h2>{selectedUser.username}</h2>
              <List
                style={{
                  display: "flex",
                  flexDirection: "column-reverse",
                  height: "70vh",
                  overflowY: "scroll",
                }}
                dataSource={messages}
                renderItem={(item) => (
                  <List.Item>
                    <div>{`${item.sender}: ${item.text}`}</div>
                  </List.Item>
                )}
              />
              <Row>
                <Col span={20}>
                  <Input
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    onPressEnter={handleSendMessage}
                    placeholder="Type your message..."
                  />
                </Col>
                <Col span={4}>
                  <Button
                    onClick={handleSendMessage}
                    type="primary"
                    style={{
                      width: "90%",
                      marginLeft: 20,
                    }}
                  >
                    Send
                  </Button>
                </Col>
              </Row>
            </div>
          ) : (
            <div>Please select a user from the sidebar to start chatting.</div>
          )}
        </Content>
      </Layout>
    </>
  );
};

export default ChatPage;
