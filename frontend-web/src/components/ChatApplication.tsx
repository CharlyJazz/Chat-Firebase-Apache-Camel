import useGetChatMessages from "@/api/hooks/useGetChatMessages";
import useSendMessage from "@/api/hooks/useSendMessage";
import { useAuth } from "@/lib/Authentication";
import {
  Avatar,
  Button,
  Col,
  Input,
  List,
  Row,
  Skeleton,
  Spin,
  Typography,
} from "antd";
import React, { useEffect, useMemo, useRef, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

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
  const paginatingRef = useRef(false);
  const scrollableDivRef = useRef<HTMLDivElement | null>(null);

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
    if (paginatingRef.current && !messagesError && messagesData.length) {
      paginatingRef.current = false;
      setMessagesForUI([...messagesForUI, ...messagesData]);
    } else if (!messagesError && messagesData.length) {
      setMessagesForUI(messagesData);
    } else if (messagesError && messagesForUI.length > 0) {
      setMessagesForUI([]);
    }
  }, [messagesData, messagesError]);

  useEffect(() => {
    if (selectedChat && paramsGetMessages?.chat_id !== selectedChat!.chat_id) {
      paginatingRef.current = false;
      setParamsGetMessages({
        chat_id: selectedChat!.chat_id,
        quantity: 10,
        time: undefined,
      });
    }
  }, [selectedChat]);

  const dataSource = useMemo(() => {
    return messagesForUI.slice().reverse();
  }, [messagesForUI]);

  const fetchMoreData = () => {
    if (paginatingRef.current || !messagesForUI.length) return;

    paginatingRef.current = true;
    const oldestMessageTime = messagesForUI[messagesForUI.length - 1].time;
    setParamsGetMessages({
      chat_id: selectedChat!.chat_id,
      quantity: 10,
      time: oldestMessageTime,
    });
  };

  const hasMore = messagesError
    ? false
    : paginatingRef.current === true
    ? false
    : messagesForUI.length >= 10;

  return (
    <WrapperDiv>
      <h2>{selectedChat?.username}</h2>

      <div
        ref={scrollableDivRef}
        id="scrollableDiv"
        style={{
          display: "flex",
          flexDirection: "column-reverse",
          height: "550px",
          overflow: "auto",
        }}
      >
        <InfiniteScroll
          dataLength={dataSource.length}
          next={fetchMoreData}
          style={{ display: "flex", flexDirection: "column-reverse" }}
          inverse={true}
          hasMore={hasMore}
          loader={<Skeleton paragraph={{ rows: 1 }} active />}
          scrollableTarget="scrollableDiv"
        >
          <List
            dataSource={dataSource}
            locale={{ emptyText: "There is not messages in this chat :(" }}
            renderItem={({ body, message_id, time_iso }) => {
              return (
                <List.Item key={message_id}>
                  <List.Item.Meta
                    avatar={
                      <Avatar size={"small"}>
                        {selectedChat!.username[0]}
                      </Avatar>
                    }
                    title={<Typography>{selectedChat!.username}</Typography>}
                    description={body}
                  />
                  <div>
                    <Typography style={{ fontSize: "11px" }}>
                      {new Date(time_iso).toLocaleTimeString()}
                    </Typography>
                  </div>
                </List.Item>
              );
            }}
          />
        </InfiniteScroll>
      </div>

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
