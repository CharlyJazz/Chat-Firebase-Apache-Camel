import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Chat",
  description: "Chat micros and front-end interactions"
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" style={{
      overflowY: 'hidden'
    }}>
      <body>{children}</body>
    </html>
  );
}
