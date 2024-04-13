import { styled } from "@mui/material/styles";
import { Box } from "@mui/material";

export const Container = styled(Box)(() => ({
  width: "100%",
  height: "100%",
  display: "flex",
  gap: "10px",
  backgroundColor: "#0C0C0C",
  backgroundRepeat: "no-repeat",
  backgroundSize: "cover",
  padding: "20px 0",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  "@media screen and (max-width: 768px)": {},
}));

export const ButtonsContainer = styled(Box)(() => ({
  width: "100%",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "10px",
  color: "white",
  "@media screen and (max-width: 768px)": {},
}));

export const InputContainer = styled(Box)(() => ({
  width: "100%",
  borderRadius: "10px",
  padding: "10px",
  boxShadow: "0px 0px 10px 1px gray",
  color: "white",
  "@media screen and (max-width: 768px)": {},
}));

export const Left = styled(Box)(() => ({
  width: "95%",
  height: "100%",
  marginTop: "50px",
  color: "white",
  "@media screen and (max-width: 768px)": {},
}));

export const ImageContainer = styled(Box)(() => ({
  width: "95%",
  minHeight: "200px",
  marginTop: "70px",
  backgroundColor: "#6965654a",
  display: "flex",
  justifyContent: "start",
  alignItems: "center",
  overflowX: "scroll",
  borderRadius: "10px",
  "&::-webkit-scrollbar": {
    width: "5px",
    backgroundColor: "#dddddd", // Change scrollbar color to gray
    borderRadius: "10px", // Round the scrollbar border
  },
  "&::-webkit-scrollbar-thumb": {
    backgroundColor: "gray", // Change thumb color to darker gray
    borderRadius: "10px", // Round the thumb border
  },
  "@media screen and (max-width: 768px)": {},
}));
