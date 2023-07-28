"use client";

import React, { useEffect, useState } from "react";
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
} from "antd";
import { useParams, useRouter } from "next/navigation";

const { Sider, Content } = Layout;

const ChatPage = () => {
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState("");

  const route = useRouter()
  const params = useParams () as {
    id?: string
  }

  const users = [
    // Replace with your list of users with id and name properties
    { id: 1, name: "Charly" },
    { id: 2, name: "Pepe" },
    { id: 3, name: "Manuel" },
    // Add more users here...
  ];

  const handleUserSelect = (user) => {
    route.replace(`/chat/${user.id}`)
  };

  const handleSendMessage = () => {
    // Send the message using your preferred method (e.g., API call)
    // and then add the new message to the messages state using setMessages()
    setMessages([...messages, { sender: "You", text: messageText }]);
    setMessageText("");
  };

  useEffect(() => {
    if (params.id) {
      setSelectedUser(users[params.id - 1])
      // Set Current User
      // Fetch messages for the selected user from your backend or mock data
      // and set them using setMessages() here
    }
  }, [])

  return (
    <>
      <Layout style={{ minHeight: "97vh" }} hasSider>
        <Sider width={200} theme="light">
          <Menu mode="inline" defaultSelectedKeys={["1"]}>
            {users.map((user) => (
              <Menu.Item key={user.id} onClick={() => handleUserSelect(user)}>
                <Space>
                  <Badge count={1} size="small">
                    <Avatar size={"small"}>{user.name[0]}</Avatar>
                  </Badge>
                  <Typography.Text>{user.name}</Typography.Text>
                </Space>
              </Menu.Item>
            ))}
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
              <h2>{selectedUser.name}</h2>
              <List
                style={{
                  display: "flex",
                  flexDirection: "column-reverse",
                  height: '70vh',
                  overflowY: 'scroll'
                }}
                dataSource={messages}
                loading={false}
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
