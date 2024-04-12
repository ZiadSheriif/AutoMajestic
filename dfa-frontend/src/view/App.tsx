import { RouterProvider } from "react-router-dom";
import router from "./routes";
import { CssBaseline } from "@mui/material";
import "./index.css";

function App() {
  return (
    <>
      <CssBaseline />
      <RouterProvider router={router}></RouterProvider>
    </>
  );
}

export default App;
