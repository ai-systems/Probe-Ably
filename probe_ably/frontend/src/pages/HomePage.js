import {
  Col,
  Container,
  Navbar,
  Row,
  Spinner,
} from "@themesberg/react-bootstrap";
import React, { useEffect, useState } from "react";

export default () => {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch("/time")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime(data.time);
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
        <Container className="position-relative">
          <Navbar.Brand href="#" className="me-lg-3">
            ProBe-Ably
          </Navbar.Brand>
        </Container>
      </Navbar>
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
    </div>
  );
};
