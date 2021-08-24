import {
  Col,
  Container,
  Navbar,
  Row,
  Spinner,
  Card,
} from "@themesberg/react-bootstrap";
import React, { useEffect, useState } from "react";
import Dashboard from "./dashboard/DashboardOverview";
import ProbeControl from "./forms/ProbeControl";
import Report from "./dashboard/Report.js"

export default () => {
  const [config, setConfig] = useState(null);
  const [isProbing, setIsProbing] = useState(false); 
  const [results, setResults] = useState(null)
  
  const startProbing = () => {
    var files = document.getElementById("config_file").files
    var formData = new FormData();
    formData.append('config_file', files[0])
    fetch("/start_probing", {method: "POST", body: formData})
    .then(setIsProbing(true))
  }

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("/results")
      .then((res) => res.json())
      .then((data)=> {setResults(data.aux_tasks)})
    }, 1000);
    return () => clearInterval(interval);
  }, [results]);
  
  return (
    <div>
    <Navbar
    variant="dark"
    expand="lg"
    bg="dark"
    className="navbar-transparent navbar-theme-primary my-2"
    >
    <Navbar.Brand href="#" className="me-md-3" style={{ padding: 5 }}>
    ProBe-Ably
    </Navbar.Brand>
    </Navbar>
    
    <main style={{ padding: 21 }}>
    <ProbeControl control={startProbing}/>
    <br/>

    {isProbing == false ? (<></>) : (
      <Card className="align-items-center">
      <Card.Header className="d-flex flex-row align-items-center flex-0">
      <div className="d-block">
      <h5 className="fw-normal mb-2">Probing Results</h5>
      </div>
      </Card.Header>
      <Report/>
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
        