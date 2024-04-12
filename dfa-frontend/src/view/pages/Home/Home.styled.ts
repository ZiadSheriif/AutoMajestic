import { styled } from "@mui/material/styles";
import { Box } from "@mui/material";

export const Container = styled(Box)(() => ({
  width: "100%",
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  gap: "10px",
  "@media screen and (max-width: 768px)": {},
}));

export const InputContainer = styled(Box)(() => ({
  width: "30%",
  height: "100%",
  "@media screen and (max-width: 768px)": {},
}));

export const ImageContainer = styled(Box)(() => ({
  width: "50%",
  minHeight: "100vh",
  backgroundColor: "#eee",
  "@media screen and (max-width: 768px)": {},
}));
