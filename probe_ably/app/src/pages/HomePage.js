import {
  Col, Container,
  Navbar,
  Row,
  Spinner,
  Card,
} from "@themesberg/react-bootstrap";

import React, { useEffect, useState } from "react";
import Report from "./dashboard/Report.js"
import ConfigDashboard from "./forms/ConfigDashboard";

export default () => {
  const [isProbing, setIsProbing] = useState(false); 
  const [results, setResults] = useState(null);
	const [taskProgress, setTaskProgress] = useState(0);
	const [modelProgress, setModelProgress] = useState(0);
	const [probesProgress, setProbesProgress] = useState(0);


  const startProbing = async (formData) => {
    setIsProbing(true);
    await fetch("/start_probing", {method: "POST", body: formData})
    .then(response => response.json())
    .then(data => setResults(data))
  }

  return (
    <div>
    <Navbar
    variant="dark"
    expand="lg"
    bg="dark"
    className="navbar-transparent navbar-theme-primary my-2"
    >
      <Container>
        <Navbar.Brand href="#" className="me-md-3" style={{ padding: 5 }}>
          Probe_Ably
        </Navbar.Brand>
      </Container>
    </Navbar>
    <main style={{ padding: 21 }}>
    <ConfigDashboard startProbing={startProbing}/>
    { isProbing === false ? (<></>) : (
      <Report taskProgress={taskProgress} 
        modelProgress={modelProgress} 
        probesProgress={probesProgress} 
        setTaskProgress={setTaskProgress}
        setModelProgress={setModelProgress}
        setProbesProgress={setProbesProgress}
        results={results}
        ></Report>
          )
    }
    </main>
    </div>
    )
  };