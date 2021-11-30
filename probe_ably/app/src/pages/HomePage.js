import {
  Col, Container,
  Navbar,
  Row,
  Spinner,
  Card,
} from "@themesberg/react-bootstrap";

import React, { useEffect, useState, useCallback } from "react";
import Dashboard from "./dashboard/DashboardOverview";
import Report from "./dashboard/Report.js"
import ConfigDashboard from "./forms/ConfigDashboard";



export default () => {
  const [config, setConfig] = useState(null);
  // const [config, setConfig] = useState(initialConfig);
  const [isProbing, setIsProbing] = useState(false); 
  const [results, setResults] = useState(null);
	const [taskProgress, setTaskProgress] = useState(0);
	const [modelProgress, setModelProgress] = useState(0);
	const [probesProgress, setProbesProgress] = useState(0);

  //   // make wrapper function to give child
  // const wrapperSetModelProgress = useCallback(val => {
  //   setModelProgress(val);
  // }, [setModelProgress]);
  // const wrapperSetProbesProgress = useCallback(val => {
  //   setProbesProgress(val);
  // }, [setProbesProgress]);

const startProbing = async () => {
    var files = document.getElementById("config_file").files;
    var formData = new FormData();
    formData.append('config_file', files[0]);
    setIsProbing(true);

    const response = await fetch("/start_probing", {method: "POST", body: formData});
    const data = await response.json();
    setResults(data);
}
  
  return (
    <div>
    <Navbar
    variant="dark"
    expand="lg"
    bg="dark"
    className="navbar-transparent navbar-theme-primary my-2"
    >
    <Navbar.Brand href="#" className="me-md-3" style={{ padding: 5 }}>
    Probe-Ably
    </Navbar.Brand>
    </Navbar>
    
    <main style={{ padding: 21 }}>
    <ConfigDashboard control={startProbing}/>
    <br/>

    { isProbing === false ? (<></>) : (
      <Card className="align-items-center">
      <Card.Header className="d-flex flex-row align-items-center flex-0">
      <div className="d-block">
      <h5 className="fw-normal mb-2">Probing Results</h5>
      </div>
      </Card.Header>
      <Report taskProgress={taskProgress} modelProgress={modelProgress} probesProgress={probesProgress} setTaskProgress={setTaskProgress} setModelProgress={setModelProgress}
      setProbesProgress={setProbesProgress}/>
      {results == null ? (
        <Row className="justify-content-md-center">
        <Col le={12} className="mb-4 mt-5 d-none d-sm-block">
        <Container>
        <Spinner
        animation="border"
        role="status"
        style={{ width: "10rem", height: "10rem" }}
        >
        <span className="sr-only">Loading...</span>
        </Spinner>
        </Container>
        </Col>
        </Row>
        ) : (
          <Dashboard aux_tasks={results} />
          )}
          </Card>)}
          </main>
          </div>
          );
        };