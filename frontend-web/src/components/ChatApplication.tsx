import React, { useEffect, useMemo, useState } from "react";
import {
  List,
  Input,
  Button,
  Row,
  Col,
  Spin,
  Typography,
  Space,
  Avatar,
} from "antd";
import useCreateChat from "@/api/hooks/useCreateChat";
import { useAuth } from "@/lib/Authentication";
import useSendMessage from "@/api/hooks/useSendMessage";
import useGetChatMessages from "@/api/hooks/useGetChatMessages";

export interface SelectedChat extends User, ChatSchema {}

function uuidTimeToDate(uuid: string): Date {
  const uuidBuffer = Buffer.from(uuid.replace(/-/g, ""), "hex");

  // Extract the timestamp part of the UUID (first 8 bytes)
  const timestampNanos =
    uuidBuffer.readUInt32BE(0) * 2 ** 32 + uuidBuffer.readUInt32BE(4);

  // Convert nanoseconds to milliseconds
  const timestampMillis = timestampNanos / 10000;

  // Calculate the base timestamp (1582-10-15 UTC) in milliseconds
  const baseTimestamp = Date.UTC(1582, 9, 15);

  // Calculate the final timestamp in milliseconds
  const finalTimestamp = baseTimestamp + timestampMillis;

  return new Date(finalTimestamp);
}

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

const LoadingChat = () => (
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

const ChatApplication: React.FC<ChatApplicationProps> = ({
  selectedChat,
  chatCreationLoading,
}) => {
  const [messagesForUI, setMessagesForUI] = useState<MessageSchema[]>([]);

  const { messageSent, sendMessage, sendMessageError, sendingMessage } =
    useSendMessage();

  const [paramsGetMessages, setParamsGetMessages] =
    useState<GetMessageValidator>();

  const { messagesData, messagesError, messagesLoading, mutate } =
    useGetChatMessages(paramsGetMessages);

  const [messageText, setMessageText] = useState("");

  const { authState } = useAuth();

  const handleSendMessage = () => {
    sendMessage(
      {
        body: messageText,
        chat_id: selectedChat!.chat_id,
        from_user: authState.id,
        to_user: String(selectedChat!.id),
      },
      mutate
    );

    setMessageText("");
  };

  if (chatCreationLoading) {
    return <LoadingChat />;
  }

  useEffect(() => {
    if (!messagesError && messagesData.length) {
      setMessagesForUI(messagesData);
    } else if (messagesError && messagesForUI.length > 0) {
      setMessagesForUI([]);
    }
  }, [messagesData, messagesError]);

  useEffect(() => {
    if (selectedChat && paramsGetMessages?.chat_id !== selectedChat!.chat_id) {
      setParamsGetMessages({
        chat_id: selectedChat!.chat_id,
        quantity: 20,
        time: undefined,
      });
    }
  }, [selectedChat]);

  const dataSource = useMemo(() => {
    return messagesForUI.slice().reverse();
  }, [messagesForUI]);

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
        loading={messagesLoading}
        dataSource={dataSource}
        renderItem={({ body, message_id, time }) => {
          return (
            <List.Item key={message_id}>
              <List.Item.Meta
                avatar={
                  <Avatar size={"small"}>{selectedChat!.username[0]}</Avatar>
                }
                title={<Typography>{selectedChat!.username}</Typography>}
                description={body}
              />
              <div>{uuidTimeToDate(time).toDateString()}</div>
            </List.Item>
          );
        }}
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
