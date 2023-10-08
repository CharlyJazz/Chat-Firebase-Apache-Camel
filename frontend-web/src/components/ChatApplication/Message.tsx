import React from "react";
import styles from "./Message.module.css";
import stc from "string-to-color";
import { Typography } from "antd";

interface MessageProps {
  label: string;
  body: string;
  time_iso: string;
  notOwner: boolean;
  firstInColumn: boolean;
}

const Message: React.FC<MessageProps> = ({
  label,
  body,
  time_iso,
  notOwner,
  firstInColumn,
}) => {
  return (
    <div
      aria-label={`${label} Says: ${body}`}
      className={styles.Message}
      style={{
        justifyContent: notOwner ? "flex-start" : "flex-end",
      }}
    >
      {firstInColumn ? (
        <div className={styles.Avatar} style={{ backgroundColor: stc(label) }}>
          <Typography.Text>{label}</Typography.Text>
        </div>
      ) : null}
      <div
        className={[
          styles.Box,
          notOwner ? styles.NotOwner : styles.Owner,
          !firstInColumn && notOwner ? styles.ExtraPaddingRight : "",
        ].join(" ")}
      >
        <p className={styles.Description}>{body}</p>
        <p className={styles.Time}>{new Date(time_iso).toLocaleString()}</p>
      </div>
    </div>
  );
};

export { Message };
