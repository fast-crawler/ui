import { BrowserRouter } from "react-router-dom";
import ReactDOM from "react-dom/client";

import App from "./App.tsx";
import "./assets/styles/_main.scss";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
