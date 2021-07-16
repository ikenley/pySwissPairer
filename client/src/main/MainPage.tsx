import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Alert } from "react-bootstrap";
import Skeleton from "react-loading-skeleton";
import Navbar from "../shared/Navbar";
import { AuthContext } from "../auth/AuthContext";
import LoginButton from "../auth/LoginButton";

const MainPage = () => {
  const { isAuthorized, hasLoaded } = useContext(AuthContext);
  const [result, setResult] = useState<any>(null);

  // Get Predictions on page load
  // useEffect(() => {
  //   if (!hasLoaded) {
  //     return;
  //   }

  //   if (!isAuthorized) {
  //     setPredictions([]);
  //     return;
  //   }

  //   axios.get("/api/prediction/by-user").then((res) => {
  //     setPredictions(res.data);
  //   });
  // }, [hasLoaded, isAuthorized, setPredictions]);

  useEffect(() => {
    axios.get("/api/status").then((res) => {
      setResult(res.data);
    });
  }, [setResult]);

  return (
    <div className="main-page">
      <Navbar />
      <main role="main" className="container-xl container-xxl pt-3 pb-5">
        <div className="jumbotron py-2 py-md-3">
          <h1 className="display-5">Swiss Pair</h1>
          <p className="lead">
            Create tournament pairings using a fancy Swiss algorithm, probably
            using blockchain or AI
            <br />
            <Link to="/about">Learn more</Link>
          </p>
        </div>
        {/* <div className="mb-3">
          <CreatePredictionModal createPrediction={createPrediction} />
        </div> */}
        {hasLoaded ? (
          isAuthorized ? (
            <div>
              Coming soon!
              <div>
                result: <code>{JSON.stringify(result)}</code>
              </div>
            </div>
          ) : (
            <div>
              <Alert variant="secondary">
                You are not logged in. Consider doing that.
                <hr />
                <LoginButton />
              </Alert>
            </div>
          )
        ) : (
          <Skeleton height={420} />
        )}

        {/* <PredictionEditor
          selPrediction={selPrediction}
          selectPrediction={selectPrediction}
          updatePrediction={updatePrediction}
          deletePrediction={deletePrediction}
        /> */}
      </main>
    </div>
  );
};

export default MainPage;
