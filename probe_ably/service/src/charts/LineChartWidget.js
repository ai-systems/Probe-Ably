import { ResponsiveScatterPlot } from "@nivo/scatterplot";
import {
  Button,
  ButtonGroup,
  Card,
  Col,
  Row,
} from "@themesberg/react-bootstrap";
import { jsPDF } from "jspdf";
import React, { useEffect, useRef } from "react";
import ReactDOM from "react-dom";
import "svg2pdf.js";

export default (props) => {
  const { title, probing_data, probing_types } = props;
  const linechartRefs = useRef([]);

  useEffect(() => {
    linechartRefs.current = linechartRefs.current.slice(0, probing_data.length);
  }, [probing_data]);

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
                      ref={(el) => (linechartRefs.current[i] = el)}
                      style={{ height: 400 }}
                      className="ct-series-g ct-major-tent"
                    >
                      <ResponsiveScatterPlot
                        colors={{ scheme: "accent" }}
                        data={p_data.chart_data}
                        margin={{ top: 60, right: 140, bottom: 70, left: 90 }}
                        xScale={{ type: "linear", min: "auto", max: "auto" }}
                        xFormat={function (e) {
                          return e;
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
                  <ButtonGroup>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      onClick={() => {
                        let data =
                          linechartRefs.current[i].children[0].children[0]
                            .children[0];
                        let image = ReactDOM.findDOMNode(data);
                        const svgData = new XMLSerializer().serializeToString(
                          image,
                        );

                        var canvas = document.createElement("canvas");

                        // Image will be scaled to the requested size.
                        // var size = data.requestedSize;
                        let width =
                          linechartRefs.current[i].children[0].children[0]
                            .clientWidth;
                        let height =
                          linechartRefs.current[i].children[0].children[0]
                            .clientHeight;

                        canvas.setAttribute("width", width);
                        canvas.setAttribute("height", height);

                        var ctx = canvas.getContext("2d");
                        ctx.fillStyle = "#FFFFFF";
                        ctx.fillRect(0, 0, 1000, 1000);

                        // var img = document.createElement("img");

                        // img.onload = () => {
                        //   ctx.drawImage(img, 0, 0, width, height);
                        //   // `download` attr is not well supported
                        //   // Will result in a download popup for chrome and the
                        //   // image opening in a new tab for others.

                        //   var a = document.createElement("a");
                        //   a.setAttribute("href", canvas.toDataURL("image/png"));
                        //   // a.setAttribute("target", "download");
                        //   // a.setAttribute("download", "chart.png");
                        //   a.click();
                        // };
                        const doc = new jsPDF({
                          orientation: "landscape",
                          format: [height, width],
                        });
                        doc
                          .svg(image, {
                            x: 0,
                            y: 0,
                            width: width,
                            height: height,
                          })
                          .then(() => {
                            // save the created pdf
                            doc.save("myPDF.pdf");
                          });

                        // img.setAttribute(
                        //   "src",
                        //   "data:image/svg+xml;base64," + btoa(svgData),
                        // );
                      }}
                    >
                      Download
                    </Button>
                  </ButtonGroup>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Card.Body>
    </Card>
  );
};
