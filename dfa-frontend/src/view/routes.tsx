import BasePage from "./pages/BasePage";
import Home from "./pages/Home/Home";
import { createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    Component: BasePage,
    children: [{ path: "", element: <Home /> }],
  },
]);

export default router;
