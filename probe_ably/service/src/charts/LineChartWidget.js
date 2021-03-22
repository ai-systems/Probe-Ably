import { ResponsiveLine } from "@nivo/line";
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
                      <ResponsiveLine
                        data={p_data.chart_data}
                        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                        xScale={{ type: "point" }}
                        yScale={{
                          type: "linear",
                          min: "auto",
                          max: "auto",
                          stacked: true,
                          reverse: false,
                        }}
                        yFormat=" >-.2f"
                        axisTop={null}
                        axisRight={null}
                        axisBottom={{
                          orient: "bottom",
                          tickSize: 5,
                          tickPadding: 5,
                          tickRotation: 0,
                          legend: p_data.x_axis,
                          legendOffset: 36,
                          legendPosition: "middle",
                        }}
                        axisLeft={{
                          orient: "left",
                          tickSize: 5,
                          tickPadding: 5,
                          tickRotation: 0,
                          legend: p_data.y_axis,
                          legendOffset: -40,
                          legendPosition: "middle",
                        }}
                        pointSize={10}
                        pointColor={{ theme: "background" }}
                        pointBorderWidth={2}
                        pointBorderColor={{ from: "serieColor" }}
                        pointLabelYOffset={-12}
                        useMesh={true}
                        legends={[
                          {
                            anchor: "bottom-right",
                            direction: "column",
                            justify: false,
                            translateX: 100,
                            translateY: 0,
                            itemsSpacing: 0,
                            itemDirection: "left-to-right",
                            itemWidth: 80,
                            itemHeight: 20,
                            itemOpacity: 0.75,
                            symbolSize: 12,
                            symbolShape: "circle",
                            symbolBorderColor: "rgba(0, 0, 0, .5)",
                            effects: [
                              {
                                on: "hover",
                                style: {
                                  itemBackground: "rgba(0, 0, 0, .03)",
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
