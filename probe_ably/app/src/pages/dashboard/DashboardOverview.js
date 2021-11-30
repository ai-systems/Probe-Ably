import { Col, Nav, Row } from "@themesberg/react-bootstrap";
import React, { useState } from "react";
import LineChartWidget from "../../charts/LineChartWidget";

export default ({ aux_tasks }) => {
  const [selectedTask, setSelectedTask] = useState(0);
  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
        <Row>
          <Col lg={12}>
            <Nav
              fill
              defaultActiveKey={aux_tasks[selectedTask].id}
              variant="pills"
              className="flex-column flex-sm-row"
            >
              {aux_tasks.map((task, i) => (
                <Nav.Item>
                  <Nav.Link
                    eventKey={task.id}
                    className="mb-sm-3 mb-md-0"
                    key={i}
                    onClick={() => setSelectedTask(i)}
                  >
                    {task.name}
                  </Nav.Link>
                </Nav.Item>
              ))}
            </Nav>
          </Col>
        </Row>
      </div>

      {aux_tasks[selectedTask].probings.map((probe, i) => (
        <Row className="justify-content-md-center">
          <Col
            xs={12}
            className="mb-4 d-none d-sm-block"
            style={{ padding: "10px" }}
          >
            <LineChartWidget
              task_name={aux_tasks[selectedTask].name}
              title={probe.model_name}
              probing_data={probe.probing_results}
              probing_types={probe.probing_types}
              key={i}
            />
          </Col>
        </Row>
      ))}
    </div>
  );
};