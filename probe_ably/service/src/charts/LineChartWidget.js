import { ResponsiveScatterPlot } from "@nivo/scatterplot";
import { Card, Col, Row } from "@themesberg/react-bootstrap";
import React, { useState } from "react";

export default (props) => {
  const { title, probing_data, probing_types } = props;
  const [probingIndex, setProbingIndex] = useState(0);
  return (
    <Card
      className="bg-secondary-alt shadow-sm"
      style={{ background: "white" }}
    >
      <Card.Header className="d-flex flex-row align-items-center flex-0">
        <div className="d-block">
          <h5 className="fw-normal mb-2">{title}</h5>
        </div>
        {/* <div className="d-flex ms-auto">
          {probing_types.map((p_type, i) => (
            <Button
              variant={i == selectedMetric ? "primary" : "secondary"}
              size="sm"
              className="me-2"
              key={i}
              onClick={() => {
                setSelectedMetric(i);
                setProbingIndex(p_type.index);
              }}
            >
              {p_type.name}
            </Button>
          ))}
        </div> */}
      </Card.Header>
      <Card.Body className="p-2">
        <Row>
          {probing_data.map((p_data, i) => (
            <Col lg={6} xs={12} md={12}>
              <Card
                className="bg-secondary-alt "
                style={{ background: "white" }}
              >
                <Card.Body className="shadow-sm border-light">
                  <h5> {p_data.y_axis}</h5>
                  <div className="ct-series-g ct-double-octave">
                    <div
                      style={{ height: 400 }}
                      className="ct-series-g ct-major-tent"
                    >
                      <ResponsiveScatterPlot
                        data={p_data.chart_data}
                        margin={{ top: 60, right: 140, bottom: 70, left: 90 }}
                        xScale={{ type: "linear", min: "auto", max: "auto" }}
                        xFormat={function (e) {
                          return e + " kg";
                        }}
                        yScale={{ type: "linear", min: "auto", max: "auto" }}
                        yFormat={function (e) {
                          return e;
                        }}
                        blendMode="multiply"
                        axisTop={null}
                        axisRight={null}
                        axisBottom={{
                          orient: "bottom",
                          tickSize: 5,
                          tickPadding: 5,
                          tickRotation: 0,
                          legend: p_data.x_axis,
                          legendPosition: "middle",
                          legendOffset: 46,
                        }}
                        axisLeft={{
                          orient: "left",
                          tickSize: 5,
                          tickPadding: 5,
                          tickRotation: 0,
                          legend: p_data.y_axis,
                          legendPosition: "middle",
                          legendOffset: -60,
                        }}
                        legends={[
                          {
                            anchor: "bottom-right",
                            direction: "column",
                            justify: false,
                            translateX: 130,
                            translateY: 0,
                            itemWidth: 100,
                            itemHeight: 12,
                            itemsSpacing: 5,
                            itemDirection: "left-to-right",
                            symbolSize: 12,
                            symbolShape: "circle",
                            effects: [
                              {
                                on: "hover",
                                style: {
                                  itemOpacity: 1,
                                },
                              },
                            ],
                          },
                        ]}
                      />
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Card.Body>
    </Card>
  );
};
