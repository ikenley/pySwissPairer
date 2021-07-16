import React, { useContext } from "react";
import classNames from "classnames";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import { NavLink } from "react-router-dom";
import { AuthContext } from "../auth/AuthContext";
import LoginButton from "../auth/LoginButton";
import LogoutButton from "../auth/LogoutButton";

type Props = {
  launchTour?: () => void;
};

const NavbarMain = ({ launchTour }: Props) => {
  const authContext = useContext(AuthContext);
  const { isLoggedIn } = authContext;

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Navbar.Brand href="/">Prediction App</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto nav-links">
          <NavLink
            className="nav-link"
            activeClassName="active"
            to="/"
            exact={true}
          >
            SwissPair
          </NavLink>
          <NavLink className="nav-link" activeClassName="active" to="/about">
            About
          </NavLink>
        </Nav>
        <Nav className="ml-auto">
          <NavItem className={classNames({ "d-none": isLoggedIn })}>
            <LoginButton />
          </NavItem>
          <NavItem className={classNames({ "d-none": !isLoggedIn })}>
            <LogoutButton />
          </NavItem>
          {/* <NavDropdown
            title={<span>Resources</span>}
            id="navbar-context-menu"
            className="navbar-context-menu"
            alignRight
          >
            {launchTour ? (
              <NavDropdown.Item onClick={handleTourClick}>
                Walkthrough
              </NavDropdown.Item>
            ) : null}
            <NavDropdown.Item target="_blank" href="/faq.pdf">
              FAQ
            </NavDropdown.Item>
            <NavDropdown.Item href="mailto:todo@todo.com">
              Contact Us
            </NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item target="_blank" href="https://www.google.com">
              Foo
            </NavDropdown.Item>
          </NavDropdown>*/}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavbarMain;
