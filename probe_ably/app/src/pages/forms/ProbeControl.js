import React from "react";
import {
  Button,
  ButtonGroup,
  Card,
  Col,
  Row,
  Form,
} from "@themesberg/react-bootstrap";

const ProbeControl = ({ control }) => {
	return(
    <Card
      className="bg-secondamyPDFry-alt shadow-sm"
      style={{ background: "white" }}
    >
      <Card.Header className="d-flex flex-row align-items-center flex-0">
      <Form>
      Choose Config File (JSON):
      <input type="file" id="config_file"/>
      </Form>
		<Button onClick={control}>
      Start Probing!
    </Button>
 	</Card.Header>
</Card>
	)
}

export default ProbeControl
