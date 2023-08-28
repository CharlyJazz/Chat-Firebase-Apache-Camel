import React, { useEffect, useState } from "react";
import { List, Input, Button, Row, Col, Spin, Typography, Space } from "antd";
import useCreateChat from "@/api/hooks/useCreateChat";
import { useAuth } from "@/lib/Authentication";

interface Message {
  sender: string;
  text: string;
}

export interface SelectedChat extends User, ChatSchema {}

interface ChatApplicationProps {
  selectedChat: SelectedChat | null;
  chatCreationLoading: boolean;
}

const WrapperDiv = ({ children }: React.PropsWithChildren) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        flex: 1,
        height: "100%",
      }}
    >
      {children}
    </div>
  );
};

const ChatApplication: React.FC<ChatApplicationProps> = ({
  selectedChat,
  chatCreationLoading,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);

  const [messageText, setMessageText] = useState("");

  const handleSendMessage = () => {
    setMessages([...messages, { sender: "You", text: messageText }]);
    setMessageText("");
  };

  useEffect(() => {
    if (selectedChat) {
    }
  }, [selectedChat]);

  if (chatCreationLoading) {
    return (
      <WrapperDiv>
        <Row style={{ margin: "auto", width: 350 }}>
          <Col span={6}>
            <Spin size="large" />
          </Col>
          <Col span={6}>
            <Typography>Loading Chat</Typography>
          </Col>
        </Row>
      </WrapperDiv>
    );
  }

  return (
    <WrapperDiv>
      <h2>{selectedChat?.username}</h2>
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
    </WrapperDiv>
  );
};

export default ChatApplication;
