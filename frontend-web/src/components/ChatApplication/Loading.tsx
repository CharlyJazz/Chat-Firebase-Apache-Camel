import { Col, Row, Spin, Typography } from "antd";

const LoadingChat = () => (
  <Row style={{ margin: "auto", width: 350 }}>
    <Col span={6}>
      <Spin size="large" />
    </Col>
    <Col span={6}>
      <Typography>Loading Chat</Typography>
    </Col>
  </Row>
);

export { LoadingChat };
