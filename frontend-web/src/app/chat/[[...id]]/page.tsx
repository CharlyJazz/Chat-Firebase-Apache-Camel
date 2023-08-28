"use client";

import useCreateChat from "@/api/hooks/useCreateChat";
import useGetCurrentUserChats from "@/api/hooks/useGetCurrentUserChats";
import useGetUsers from "@/api/hooks/useGetUsers"; // Update the path as per your project structure
import ChatApplication, { SelectedChat } from "@/components/ChatApplication";
import { useAuth } from "@/lib/Authentication";
import { Avatar, Badge, Layout, Menu, Space, Spin, Typography } from "antd";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const { Sider, Content } = Layout;

const ChatPage = () => {
  const [selectedFriend, setSelectedChat] = useState<SelectedChat | null>(null);

  const [finishedParamSetup, setFinishedParamSetup] = useState(false);

  const params = useParams() as { id?: string[] };

  const {
    authState: { username: currentUsername, id: currentUserId },
  } = useAuth();
  const { usersData, usersError, usersLoading } = useGetUsers();
  const { chatsData, chatsError, chatsLoading } = useGetCurrentUserChats();
  const { chatCreated, chatCreationLoading, createChat, errorCreatingChat } =
    useCreateChat();

  const silentRedirectToChat = (userId: string | number) => {
    const newPath = `/chat/${userId}`;
    window.history.replaceState({}, "", newPath);
  };

  const handleUserSelect = async (userToChat: User) => {
    const friendChat = chatsData?.find(
      (chat) =>
        chat.users_id.includes(String(currentUserId)) &&
        chat.users_id.includes(String(userToChat.id))
    );

    if (friendChat) {
      setSelectedChat({
        ...userToChat,
        ...friendChat,
      });
      silentRedirectToChat(userToChat.id);
    } else {
      try {
        const friendChat = await createChat({
          users_id: [currentUserId, String(userToChat.id)],
          users_name: [currentUsername, userToChat.username],
        });
        if (friendChat) {
          setSelectedChat({
            ...userToChat,
            ...friendChat,
          });
        }
        silentRedirectToChat(userToChat.id);
      } catch (error) {}
    }
  };

  useEffect(() => {
    if (
      chatsData.length &&
      usersData.length &&
      params.id &&
      typeof params.id[0] === "string" &&
      finishedParamSetup === false
    ) {
      const currentUserId = params.id[0];
      const user = usersData.find(
        (user) => user.id === parseInt(currentUserId)
      );

      if (user) {
        setFinishedParamSetup(true);
        handleUserSelect(user);
      }
    }
  }, [params.id, usersData, chatsData]);

  if (usersLoading && chatsLoading) {
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
              height: "94vh",
              overflow: "auto",
              marginTop: "10px",
            }}
          >
            {!usersError &&
              usersData.map((user) => {
                const friendOrUnknow = chatsData?.some((chat) =>
                  chat.users_id.includes(String(user.id))
                );
                return (
                  <Menu.Item
                    key={user.id}
                    onClick={() => handleUserSelect(user)}
                  >
                    <Space>
                      <Badge
                        size="small"
                        count={friendOrUnknow ? "" : "?"}
                        color={friendOrUnknow ? "green" : "yellow"}
                      >
                        <Avatar size={"small"}>{user.username[0]}</Avatar>
                      </Badge>
                      <Typography.Text>{user.username}</Typography.Text>
                    </Space>
                  </Menu.Item>
                );
              })}
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
          {selectedFriend ? (
            <ChatApplication
              selectedChat={selectedFriend}
              chatCreationLoading={chatCreationLoading}
            />
          ) : (
            <div>Please select a user from the sidebar to start chatting.</div>
          )}
        </Content>
      </Layout>
    </>
  );
};

export default ChatPage;
