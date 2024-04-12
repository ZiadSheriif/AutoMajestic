import { Box, Typography } from "@mui/material";

const Footer = () => {
  return (
    <Box
      sx={{
        height: "50px",
        width: "100%",
        backgroundColor: "#481E14",
        padding: "0 20px",
        display: "flex",
        alignItems: "center",
      }}
    >
      <Typography sx={{ color: "white", fontSize: "1rem" }}>
        &copy; Romy & Ziad 2024
      </Typography>
    </Box>
  );
};

export default Footer;
