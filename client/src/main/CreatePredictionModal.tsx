import React, { useState, useContext, useCallback } from "react";
import { Button, Modal, Form, Row, Col } from "react-bootstrap";
import numeral from "numeral";
import { AuthContext } from "../auth/AuthContext";
import { Prediction, defaultPrediction } from "../types";

type Props = {
  createPrediction: (prediction: Prediction) => Promise<any>;
};

const CreatePredictionModal = ({ createPrediction }: Props) => {
  const { isAuthorized } = useContext(AuthContext);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [prediction, setPrediction] = useState<Prediction>(defaultPrediction);

  const openModal = useCallback(() => {
    setShowModal(true);
  }, [setShowModal]);
  const closeModal = useCallback(() => {
    setShowModal(false);
  }, [setShowModal]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      let { name, type } = e.currentTarget;
      let value: any = e.currentTarget.value;

      if (type === "date") {
        value = new Date(value);
      }

      setPrediction((p) => {
        return { ...p, [name]: value };
      });
    },
    [setPrediction]
  );

  const handleCreate = useCallback(async () => {
    await createPrediction(prediction);
    closeModal();
  }, [prediction, closeModal, createPrediction]);

  if (!isAuthorized) {
    return null;
  }

  return (
    <div className="create-prediction-editor">
      <Button variant="primary" onClick={openModal}>
        <i className="fas fa-plus" /> Create Prediction
      </Button>

      <Modal show={showModal} onHide={closeModal} size="lg" backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>Create Prediction</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group as={Row} controlId="formCreateName">
              <Form.Label column sm={2}>
                Name
              </Form.Label>
              <Col sm={10}>
                <Form.Control
                  type="input"
                  name="name"
                  value={prediction.name}
                  onChange={handleChange}
                  placeholder="Odds a coin flip will come up heads..."
                />
              </Col>
            </Form.Group>
            <Form.Group
              as={Row}
              controlId="formCreateProbability"
              className="align-items-center"
            >
              <Form.Label column sm={2}>
                Probability
              </Form.Label>
              <Col sm={1}>{numeral(prediction.probability).format("0%")}</Col>
              <Col sm={9}>
                <Form.Control
                  type="range"
                  min={0}
                  max={1}
                  step={0.01}
                  name="probability"
                  value={prediction.probability}
                  onChange={handleChange}
                />
              </Col>
            </Form.Group>
            <Form.Group as={Row} controlId="formCreateRevisitOn">
              <Form.Label column sm={2}>
                Revisit On
              </Form.Label>
              <Col sm={10}>
                <Form.Control
                  type="date"
                  name="revisitOn"
                  value={prediction.revisitOn.toISOString().substr(0, 10)}
                  onChange={handleChange}
                  placeholder="Odds a coin flip will come up heads..."
                />
              </Col>
            </Form.Group>
            <Form.Group as={Row} controlId="formCreateDescription">
              <Form.Label column sm={2}>
                Description
              </Form.Label>
              <Col sm={10}>
                <Form.Control
                  as="textarea"
                  name="description"
                  value={prediction.description}
                  onChange={handleChange}
                  placeholder="Any additional detail..."
                />
              </Col>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-dark" onClick={closeModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleCreate}>
            Create
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default CreatePredictionModal;
