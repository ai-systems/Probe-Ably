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


const Report = ({ taskProgress, modelProgress, probesProgress, setTaskProgress, setModelProgress, setProbesProgress, results, isProbing }) => {

const imgStyle = {
  paddingRight: '3px',
  height: '90%',
}
    useEffect(() => {
      const interval = setInterval(() => {
        if (isProbing) {
        fetch("/task_progress")
        .then((res) => res.json())
        .then(progress => {setTaskProgress(progress)})
        }
      }, 500);

      return () => clearInterval(interval);
    }, [taskProgress, setTaskProgress, isProbing]);

    useEffect(() => {
      const interval = setInterval(() => {
        if (isProbing) {
        fetch("/model_progress")
        .then((res) => res.json())
        .then((prog)=>{setModelProgress(prog)});
        }
      }, 500);

      return () => clearInterval(interval);
    }, [modelProgress, setModelProgress, isProbing]);

    useEffect(() => {
      const interval = setInterval(() => {
        if (isProbing) {
        fetch("/probes_progress")
        .then((res) => res.json())
        .then((prog)=>{setProbesProgress(prog)});
        }
      }, 500);

      return () => clearInterval(interval);
    }, [probesProgress, setProbesProgress, isProbing]);

    return (
      <Container>
        <Card className="align-items-center">
        {results == null ? (
          isProbing == false ? (<></>) : (
          <Row className="justify-content-md-center">
          <Col le={12} className="mb-4 mt-5 d-none d-sm-block">
          <ProgressBar taskProgress={taskProgress} modelProgress={modelProgress} probesProgress={probesProgress}/>
          <Container>
          {/* <img style={imgStyle} src={fireparrot}/> */}
          <center>
          <Spinner
          animation="border"
          role="status"
          style={{ width: "5rem", height: "5rem" }}
          >
          </Spinner>
          </center>
          </Container>
          </Col>
          </Row>
          )) : (
        <Container>
          <Card.Header className="d-flex flex-row align-items-center flex-0">
          <div className="d-block">
          <h5 className="fw-normal mb-2">Probing Results</h5>
          </div>
          </Card.Header>
          <Dashboard tasks={results} />
        </Container>
        )}
        </Card>
      </Container>
      )
    };


export default Report
