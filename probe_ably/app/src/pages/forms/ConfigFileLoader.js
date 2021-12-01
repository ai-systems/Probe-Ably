import React from "react";
import {
  Button,
  Col,
  Row,
  Form,
  Container
} from "@themesberg/react-bootstrap";

const ConfigFileLoader = ({ control }) => {
	return(
    <Container>
      Choose Config File (JSON):
    <Row>
    <Col>
      <Form.Control type="file" id="config_file"/>
    </Col>
    <Col>
      <Button onClick={control}>
        Start Probing!
      </Button>
      </Col>
      </Row>
      <p>
        (File Format Guide)
        </p>
   </Container>
	)
}
export default ConfigFileLoader
