import { styled } from "@mui/material/styles";
import { Box } from "@mui/material";

export const Container = styled(Box)(() => ({
  width: "100%",
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  gap: "10px",
  "@media screen and (max-width: 768px)": {
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
}));

export const ButtonsContainer = styled(Box)(() => ({
  width: "100%",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "10px",
  "@media screen and (max-width: 768px)": {},
}));

export const InputContainer = styled(Box)(() => ({
  width: "30%",
  height: "100%",
  borderRadius: "10px",
  padding: "10px",
  boxShadow: "0px 0px 10px 1px gray",
  "@media screen and (max-width: 768px)": {
    width: "100%",
  },
}));

export const ImageContainer = styled(Box)(() => ({
  width: "50%",
  minHeight: "100vh",
  backgroundColor: "#eee",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  "@media screen and (max-width: 768px)": {
    width: "100%",
  },
}));
