import React, { useState } from "react";
import {
    Card,
    Col,
    Row,
    Tab,
    Nav,
    Form,
    Container
} from "@themesberg/react-bootstrap";
import ConfigFileLoader from "./ConfigFileLoader";
import ConfigForm from "./ConfigForm"

const ConfigDashboard = ({ startProbing }) => {
    return(
        <div>
        <Container>
            <Card>
    <Tab.Container defaultActiveKey="config_manual">
  <Row>
    <Col lg={12}>
      <Nav className="nav-tabs">
        <Nav.Item>
          <Nav.Link eventKey="config_manual" className="mb-sm-3 mb-md-0">
              Configure Probing 
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey="config_file" className="mb-sm-3 mb-md-0">
              Load Config File
          </Nav.Link>
        </Nav.Item>
      </Nav>
    </Col>
    <Col lg={12}>
      <Tab.Content>
        <Tab.Pane eventKey="config_manual" className="py-4">
          <ConfigForm startProbing={startProbing}></ConfigForm>
        </Tab.Pane>
        <Tab.Pane eventKey="config_file" className="py-4">
             <ConfigFileLoader startProbing={startProbing}/>
        </Tab.Pane>
      </Tab.Content>
    </Col>
  </Row>
    </Tab.Container>
    </Card>
    </Container>
        </div>
        )
    }
    
    export default ConfigDashboard