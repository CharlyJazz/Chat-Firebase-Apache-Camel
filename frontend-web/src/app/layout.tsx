import { AuthProvider } from "@/lib/Authentication";
import type { Metadata } from "next";
import StyledComponentsRegistry from "../lib/AntdRegistry";

export const metadata: Metadata = {
  title: "Chat",
  description: "Chat micros and front-end interactions",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      style={{
        overflowY: "hidden",
      }}
    >
      <body>
        <StyledComponentsRegistry>
          <AuthProvider>{children}</AuthProvider>
        </StyledComponentsRegistry>
      </body>
    </html>
  );
}
