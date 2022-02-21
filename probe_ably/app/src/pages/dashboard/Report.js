import React, { useEffect } from "react";
import ProgressBar from "./ProgressBar"
import Dashboard from "./DashboardOverview";
import fireparrot from "../../assets/fireparrot.gif"
import {
  Col, Container,
  Navbar,
  Row,
  Spinner,
  Card,
  Nav,
} from "@themesberg/react-bootstrap";


const Report = ({ taskProgress, modelProgress, probesProgress, setTaskProgress, setModelProgress, setProbesProgress, results, setResults }) => {

const imgStyle = {
  paddingRight: '3px',
  height: '90%',
}

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/task_progress")
        .then((res) => res.json())
        .then(progress => {setTaskProgress(progress)})
      }, 500);

      return () => clearInterval(interval);
    }, [taskProgress, setTaskProgress]);

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/model_progress")
        .then((res) => res.json())
        .then((prog)=>{setModelProgress(prog)});
      }, 500);
      return () => clearInterval(interval);
    }, [modelProgress, setModelProgress]);

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/probes_progress")
        .then((res) => res.json())
        .then((prog)=>{setProbesProgress(prog)});
      }, 500);
      return () => clearInterval(interval);
    }, [probesProgress, setProbesProgress]);

    return (
      <Container>
      <Card className="align-items-center">
      {/* <Card.Header className="d-flex flex-row align-items-center flex-0">
      <div className="d-block">
      <h5 className="fw-normal mb-2">Probing Results</h5>
      </div>
      </Card.Header> */}
      <ProgressBar taskProgress={taskProgress} modelProgress={modelProgress} probesProgress={probesProgress}/>
      {results == null ? (
        <Row className="justify-content-md-center">
        <Col le={12} className="mb-4 mt-5 d-none d-sm-block">
        <Container>
        {/* <img style={imgStyle} src={fireparrot}/> */}
        <Spinner
        animation="border"
        role="status"
        style={{ width: "5rem", height: "5rem" }}
        >
        <center>
        <span className="sr-only">Loading...</span>
        </center>
        </Spinner>
        </Container>
        </Col>
        </Row>
        ) : (
          <Dashboard tasks={results} />
          )}
          </Card>
          </Container>)
    };

export default Report
