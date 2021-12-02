import React from "react";
import {
  Button,
  Col,
  Row,
  Form,
  Container
} from "@themesberg/react-bootstrap";

const ConfigFileLoader = ({ startProbing }) => {

  const submit = async () => {
    var files = document.getElementById("config_file").files;
    var formData = new FormData();
    formData.append('config_file', files[0]);
    startProbing(formData);
  }

	return(
    <Container>
      Choose Config File (JSON):
    <Row>
    <Col>
      <Form.Control type="file" id="config_file"/>
    </Col>
    <Col>
      <Button onClick={submit}>
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
