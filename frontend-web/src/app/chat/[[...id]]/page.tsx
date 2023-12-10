"use client";
import useCreateChat from "@/api/hooks/useCreateChat";
import useGetCurrentUserChats from "@/api/hooks/useGetCurrentUserChats";
import useGetUsers from "@/api/hooks/useGetUsers";
import ChatApplication, { SelectedChat } from "@/components/ChatApplication";
import { useAuth } from "@/lib/Authentication";
import { Avatar, Badge, Button, Layout, Menu, Space, Typography } from "antd";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import stc from "string-to-color";

const { Sider, Content } = Layout;

const ChatPage = () => {
  // State to store selected friend's chat information
  const [selectedChat, setSelectedChat] = useState<SelectedChat | null>(null);

  // State to track if parameter setup is finished
  const [finishedParamSetup, setFinishedParamSetup] = useState(false);

  // Get parameters from URL
  const params = useParams() as { id?: string[] };

  const route = useRouter();

  // Get authenticated user's information from Auth context
  const {
    authState: { username: currentUsername, id: currentUserId },
    logout,
  } = useAuth();

  // Fetch users data
  const { usersData, usersError, usersLoading } = useGetUsers();

  // Fetch current user's chats data
  const { chatsData, chatsError, chatsLoading } = useGetCurrentUserChats();

  // Use the createChat function from the hook
  const { chatCreated, chatCreationLoading, createChat, errorCreatingChat } =
    useCreateChat();

  // Function to update URL path without triggering a navigation
  const silentRedirectToChat = (userId: string | number) => {
    const newPath = `/chat/${userId}`;
    window.history.replaceState({}, "", newPath);
  };

  // Function to handle user selection
  const handleUserSelect = async (userToChat: User) => {
    // Check if there's an existing chat with the selected friend
    const friendChat = chatsData?.find(
      (chat) =>
        chat.users_id.includes(String(currentUserId)) &&
        chat.users_id.includes(String(userToChat.id))
    );

    if (friendChat) {
      // Set selected chat and update URL path
      setSelectedChat({
        ...userToChat,
        ...friendChat,
      });
      silentRedirectToChat(userToChat.id);
    } else {
      try {
        // Create a new chat with the selected friend
        const friendChat = await createChat({
          users_id: [currentUserId, String(userToChat.id)],
          users_name: [currentUsername, userToChat.username],
        });

        if (friendChat) {
          // Set selected chat and update URL path
          setSelectedChat({
            ...userToChat,
            ...friendChat,
          });
        }
        silentRedirectToChat(userToChat.id);
      } catch (error) {
        // Handle error
      }
    }
  };

  // Effect to handle URL parameter setup
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

  const handleLogout = () => {
    logout();
    route.replace("/");
  };

  return (
    <>
      {/* Layout setup */}
      <Layout style={{ minHeight: "97vh" }} hasSider>
        <Sider width={250} theme="light">
          {/* Sidebar menu */}
          <Typography style={{ marginLeft: 25 }}>
            Good day, {currentUsername}.
          </Typography>
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            style={{
              height: "80vh",
              overflow: "auto",
              marginTop: "12px",
            }}
          >
            {!usersError &&
              usersData
                .filter((n) => String(n.id) !== String(currentUserId))
                .map((user) => {
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
                          <Avatar
                            size={"small"}
                            style={{
                              backgroundColor: stc(user.username + user.id),
                            }}
                          >
                            {user.username[0]}
                          </Avatar>
                        </Badge>
                        <Typography.Text>{user.username}</Typography.Text>
                      </Space>
                    </Menu.Item>
                  );
                })}
            {usersError ? (
              <Space>
                {/* Display error message */}
                <Typography.Text>
                  There was an error getting the users
                </Typography.Text>
              </Space>
            ) : null}
          </Menu>
          <Button
            onClick={handleLogout}
            style={{ margin: "25px 0 0 25px" }}
            type="dashed"
          >
            Logout
          </Button>
        </Sider>
        <Content style={{ padding: "24px", background: "#f0f2f5" }}>
          {/* Display chat application or select user message */}
          {selectedChat ? (
            <ChatApplication
              selectedChat={selectedChat}
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
