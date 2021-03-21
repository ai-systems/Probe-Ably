// =========================================================
// * Volt React Dashboard
// =========================================================

// * Product Page: https://themesberg.com/product/dashboard/volt-react
// * Copyright 2021 Themesberg (https://www.themesberg.com)
// * Official Repository: https://github.com/themesberg/volt-react-dashboard
// * License: MIT License (https://themesberg.com/licensing)

// * Designed and coded by https://themesberg.com

// =========================================================

// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal.

// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import React from "react";
import "react-datetime/css/react-datetime.css";
import ReactDOM from "react-dom";
import HomePage from "./pages/HomePage";
// core styles
import "./scss/volt.scss";

ReactDOM.render(
  <div>
    {/* <ScrollToTop /> */}
    <HomePage />
  </div>,
  document.getElementById("root"),
);
