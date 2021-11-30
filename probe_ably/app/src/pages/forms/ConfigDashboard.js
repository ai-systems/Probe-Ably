import React, { useState } from "react";
import {
  Button,
  ButtonGroup,
  Card,
  Col,
  Row,
  Nav,
  Form,
  Accordion,
  Container
} from "@themesberg/react-bootstrap";
import ConfigFileLoader from "./ConfigFileLoader";

const ConfigDashboard = ({ control }) => {
    const tabNames = ['Configure Probing', 'Load Config File File']
    const [selectedTask, setSelectedTask] = useState(0);

	return(
        <div>
        <Container>
        <Accordion defaultActiveKey="0">
        <Accordion.Item eventKey="0">
            <Accordion.Header>Configure Probing</Accordion.Header>
            <Accordion.Body>
            </Accordion.Body>
        </Accordion.Item>
        <Accordion.Item eventKey="1">
            <Accordion.Header>Alternatively, Load Config File:</Accordion.Header>
            <Accordion.Body>
                <ConfigFileLoader control={control}/>
            </Accordion.Body>
        </Accordion.Item>
        </Accordion>
        </Container>
      </div>
	)
}

export default ConfigDashboard