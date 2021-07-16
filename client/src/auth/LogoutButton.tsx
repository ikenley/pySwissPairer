import React, { useContext } from "react";
import { GoogleLogout } from "react-google-login";
import { AuthContext } from "./AuthContext";

const LogoutButton = () => {
  const authContext = useContext(AuthContext);

  return (
    <GoogleLogout
      clientId="40576505573-35gusqr80mdhv8v4vmpvqmdr9g1t40kq.apps.googleusercontent.com"
      buttonText="Logout"
      onLogoutSuccess={authContext.handleLogout}
    />
  );
};

export default LogoutButton;
