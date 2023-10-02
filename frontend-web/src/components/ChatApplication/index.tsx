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
  Typography,
} from "antd";
import { collection, onSnapshot, query, where } from "firebase/firestore";
import React, { useEffect, useMemo, useRef, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { db } from "../../firebase/firebaseConfig";
import { LoadingChat } from "./Loading";
import { WrapperDiv } from "./WrapperDiv";

export interface SelectedChat extends User, ChatSchema {}

interface ChatApplicationProps {
  selectedChat: SelectedChat | null;
  chatCreationLoading: boolean;
}

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
    const createMessagePayload: CreateMessagePayload = {
      body: messageText,
      chat_id: selectedChat!.chat_id,
      from_user: authState.id,
      to_user: String(selectedChat!.id),
    };

    sendMessage(createMessagePayload, mutate);

    setMessageText("");
  };

  useEffect(() => {
    if (selectedChat && messagesForUI.length) {
      const q = query(
        collection(db, "messages"),
        where("chat_id", "==", selectedChat.chat_id),
        where("from_user", "==", String(selectedChat.id)),
        where("latest_message_time_iso", ">", messagesForUI[0].time_iso)
      );

      const unsubscribe = onSnapshot(q, (querySnapshot) => {
        querySnapshot.docChanges().forEach((change) => {
          if (change.type === "added") {
            const docData = change.doc.data() as FirestoreNewMessageContract;
            if (docData.list_of_messages && docData.list_of_messages.length) {
              const mappedIds = messagesForUI.map((msg) => msg.time_iso);
              if (!mappedIds.includes(docData.latest_message_time_iso)) {
                console.log(
                  "Injecting new messages from firestore into the state..."
                );

                const messagesSorted = docData.list_of_messages.sort((a, b) => {
                  const timeA = new Date(a.time_iso).getTime();
                  const timeB = new Date(b.time_iso).getTime();
                  return timeB - timeA;
                });

                setMessagesForUI([...messagesSorted, ...messagesForUI]);
              }
            }
          }
        });
      });

      return () => {
        unsubscribe();
      };
    }
  }, [selectedChat, messagesForUI]);

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

  if (chatCreationLoading) {
    return (
      <WrapperDiv>
        <LoadingChat />
      </WrapperDiv>
    );
  }

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
            renderItem={({ body, message_id, time_iso, from_user }, index) => {
              const notOwner = String(selectedChat?.id) === from_user;
              const label = notOwner ? selectedChat!.username[0] : "You";
              return (
                <List.Item key={message_id} style={{ border: "none" }}>
                  <List.Item.Meta
                    avatar={<Avatar size={"small"}>{label}</Avatar>}
                    title={<Typography>{label}</Typography>}
                    description={body}
                  />
                  <div>
                    <Typography style={{ fontSize: "10px" }}>
                      {new Date(time_iso).toLocaleString()}
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
