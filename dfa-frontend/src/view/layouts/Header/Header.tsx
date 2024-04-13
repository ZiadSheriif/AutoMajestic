import { Box, Typography } from "@mui/material";

const Header = () => {
  return (
    <Box
      sx={{
        height: "50px",
        width: "100%",
        backgroundColor: "#9B3922",
        padding: "0 50px",
      }}
    >
      <Typography sx={{ color: "white", fontSize: "2rem" }}>
        <i>AutoMajestic</i>
      </Typography>
    </Box>
  );
};

export default Header;
