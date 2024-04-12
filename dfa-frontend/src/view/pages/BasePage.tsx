import { Box } from "@mui/system";
import { Outlet } from "react-router";
import { Toaster } from "react-hot-toast";
import Header from "../layouts/Header/Header";
import Footer from "../layouts/Footer/Footer";
const BasePage = () => {
  return (
    <>
      {" "}
      <Header />
      <Box
        sx={{
          position: "relative",
          minHeight: "100vh",
          width: "100vw",
        }}
      >
        <Box sx={{ minHeight: "100%", width: "100%" }}>
          <Outlet />
        </Box>
      </Box>
      <Footer />
      <Toaster
        position="top-center"
        gutter={12}
        containerStyle={{
          margin: "8px",
        }}
        toastOptions={{
          success: {
            duration: 3000,
          },
          error: {
            duration: 5000,
          },
          style: {
            fontSize: "16px",
            padding: "16px 24px",
            fontWeight: "500",
            color: "var(--color-grey-700)",
          },
        }}
      />
    </>
  );
};

export default BasePage;
