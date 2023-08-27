import React, { useState } from "react";
import { List, Input, Button, Row, Col } from "antd";

interface Message {
  sender: string;
  text: string;
}

interface ChatContentProps {
  selectedUser: User | null;
}

const ChatContent: React.FC<ChatContentProps> = ({ selectedUser }) => {
  const [messages, setMessages] = useState<Message[]>([]); // Mock messages state
  const [messageText, setMessageText] = useState("");

  const handleSendMessage = () => {
    setMessages([...messages, { sender: "You", text: messageText }]);
    setMessageText("");
  };

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
      <h2>{selectedUser?.username}</h2>
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
  );
};

export default ChatContent;
