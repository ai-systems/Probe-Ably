import React from "react";
import {
  Button,
  ButtonGroup,
  Card,
  Col,
  Row,
} from "@themesberg/react-bootstrap";

const ProbeControl = ({ control }) => {
	return(
    <Card
      className="bg-secondamyPDFry-alt shadow-sm"
      style={{ background: "white" }}
    >
      <Card.Header className="d-flex flex-row align-items-center flex-0">
		<Button onClick={control}/>
 	</Card.Header>
</Card>
	)
}

export default ProbeControl
