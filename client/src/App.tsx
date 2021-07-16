import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Footer from "./shared/Footer";
import { AuthContextProvider } from "./auth/AuthContext";
import ScrollToTop from "./shared/ScrollToTop";
import AboutPage from "./about/AboutPage";
import MainPage from "./main/MainPage";

const App = () => {
  return (
    <AuthContextProvider>
      <Router>
        <div className="app">
          <ScrollToTop />
          <Switch>
            <Route path="/about">
              <AboutPage />
            </Route>
            <Route path="/">
              <MainPage />
            </Route>
          </Switch>

          <Footer />
        </div>
      </Router>
    </AuthContextProvider>
  );
};

export default App;
