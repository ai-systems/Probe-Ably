import {
  Col,
  Container,
  Navbar,
  Row,
  Spinner,
} from "@themesberg/react-bootstrap";
import React, { useEffect, useState } from "react";
import Dashboard from "./dashboard/DashboardOverview";

export default () => {
  const [auxTasks, setAuxTasks] = useState(null);

  useEffect(() => {
    fetch("/sample")
      .then((res) => res.json())
      .then((data) => {
        setAuxTasks(data.aux_tasks);
      });
  }, []);

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
      <main style={{ padding: 20 }}>
        {auxTasks == null ? (
          <Row className="justify-content-md-center">
            <Col lg={12} className="mb-4 d-none d-sm-block">
              <Container>
                <Spinner
                  animation="border"
                  role="status"
                  style={{ width: "10rem", height: "10rem" }}
                >
                  <span class="sr-only">Loading...</span>
                </Spinner>
              </Container>
            </Col>
          </Row>
        ) : (
          <Dashboard aux_tasks={auxTasks} />
        )}
      </main>
    </div>
  );
};
