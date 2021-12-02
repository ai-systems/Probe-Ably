import { Button, Card, Col, Form, Row } from "@themesberg/react-bootstrap";
import React, { useState } from "react";

const ConfigForm  = ({ startProbing }) => {
    const submit = async () => {
        var files = document.getElementById("config_file").files;
        var formData = new FormData();
        formData.append('config_file', files[0]);
        startProbing(formData);
    }

    return(
    <div>
       <Row style={{ padding: 10 }}>
       </Row>
    </div>
    )
};
//   return (
//     <div>
//       <Row style={{ padding: 10 }}>
//         <Col lg={12}>
//           <Form>
//             <Form.Group className="mb-3">
//               <Form.Label>Task Name</Form.Label>
//               <Form.Control type="text" placeholder="Task Name" />
//             </Form.Group>
//             <Button variant="outline-primary" size="sm">
//               Add Task
//             </Button>
//           </Form>
//         </Col>
//       </Row>

//       {tasks.map((task_data, i) => (
//         <Row style={{ padding: 30 }} key={i}>
//           <Card
//             className="bg-secondary-alt shadow-sm"
//             style={{ background: "white" }}
//           >
//             <Card.Header className="d-flex flex-row align-items-center flex-0">
//               <div className="d-block">
//                 <h5 className="fw-normal mb-2">{task_data.task_name}</h5>
//               </div>
//               <Col md={{ span: 4, offset: 4 }}>
//                 <Button variant="outline-danger" size="sm">
//                   Remove Task
//                 </Button>
//               </Col>
//             </Card.Header>
//             <Card.Body className="p-2">
//               <Form>
//                 <Form.Group className="mb-3">
//                   <Form.Label>Model Name</Form.Label>
//                   <Form.Control type="text" placeholder="Model Name" />
//                 </Form.Group>

//                 <Form.Group className="mb-3">
//                   <Form.Label>Representations</Form.Label>
//                   <Form.Control
//                     type="file"
//                     placeholder="Representations Path"
//                   />
//                 </Form.Group>

//                 <Form.Group className="mb-3">
//                   <Form.Label>Representations Labels</Form.Label>
//                   <Form.Control
//                     type="file"
//                     placeholder="Representations Labels"
//                   />
//                 </Form.Group>
//                 <Form.Group className="mb-3">
//                   <Form.Label>Control Task Class</Form.Label>
//                   <Form.Control
//                     type="text"
//                     placeholder="Control Task Class"
//                     value="probe_ably.tasks.control_task"
//                   />
//                 </Form.Group>
//                 <Button variant="outline-primary" size="sm">
//                   Add Model
//                 </Button>
//               </Form>
//             </Card.Body>
//           </Card>
//         </Row>
//       ))}

//       <Row style={{ padding: 10 }}>
//         <Col lg={4}>
//           <Button variant="primary" className="m-1" size="sm">
//             Launch Probe
//           </Button>
//           <Button variant="secondary" className="m-1" size="sm">
//             Reset Form
//           </Button>
//         </Col>
//       </Row>
//     </div>
//   );
// };

//   return (
//     <div>
//       <Row style={{ padding: 10 }}>
//         <Col lg={12}>
//           <Form>
//             <Form.Group className="mb-3">
//               <Form.Label>Task Name</Form.Label>
//               <Form.Control type="text" placeholder="Task Name" />
//             </Form.Group>
//             <Button variant="outline-primary" size="sm">
//               Add Task
//             </Button>
//           </Form>
//         </Col>
//       </Row>

//       {tasks.map((task_data, i) => (
//         <Row style={{ padding: 30 }} key={i}>
//           <Card
//             className="bg-secondary-alt shadow-sm"
//             style={{ background: "white" }}
//           >
//             <Card.Header className="d-flex flex-row align-items-center flex-0">
//               <div className="d-block">
//                 <h5 className="fw-normal mb-2">{task_data.task_name}</h5>
//               </div>
//               <Col md={{ span: 4, offset: 4 }}>
//                 <Button variant="outline-danger" size="sm">
//                   Remove Task
//                 </Button>
//               </Col>
//             </Card.Header>
//             <Card.Body className="p-2">
//               <Form>
//                 <Form.Group className="mb-3">
//                   <Form.Label>Model Name</Form.Label>
//                   <Form.Control type="text" placeholder="Model Name" />
//                 </Form.Group>

//                 <Form.Group className="mb-3">
//                   <Form.Label>Representations</Form.Label>
//                   <Form.Control
//                     type="file"
//                     placeholder="Representations Path"
//                   />
//                 </Form.Group>

//                 <Form.Group className="mb-3">
//                   <Form.Label>Representations Labels</Form.Label>
//                   <Form.Control
//                     type="file"
//                     placeholder="Representations Labels"
//                   />
//                 </Form.Group>
//                 <Form.Group className="mb-3">
//                   <Form.Label>Control Task Class</Form.Label>
//                   <Form.Control
//                     type="text"
//                     placeholder="Control Task Class"
//                     value="probe_ably.tasks.control_task"
//                   />
//                 </Form.Group>
//                 <Button variant="outline-primary" size="sm">
//                   Add Model
//                 </Button>
//               </Form>
//             </Card.Body>
//           </Card>
//         </Row>
//       ))}

//       <Row style={{ padding: 10 }}>
//         <Col lg={4}>
//           <Button variant="primary" className="m-1" size="sm">
//             Launch Probe
//           </Button>
//           <Button variant="secondary" className="m-1" size="sm">
//             Reset Form
//           </Button>
//         </Col>
//       </Row>
//     </div>
//   );
// };
export default ConfigForm