import { styled } from "@mui/material/styles";
import { Typography, Box } from "@mui/material";

interface ContainerProps {
  isSplitted: boolean | undefined;
  login: boolean;
  resetBorder: boolean;
}

export const Container = styled(Box)<ContainerProps>(
  ({ isSplitted, login, resetBorder }) => ({
    display: "flex",
    flexDirection: "column",
    width: isSplitted ? "47%" : "100%",
    alignSelf: "stretch",
    margin: "8px 0",

    input: {
      border: resetBorder ? "none" : "1px solid silver",

      height: "2.4rem",
      borderRadius: isSplitted ? "8px" : "8px 8px 8px 8px",
      backgroundColor: login ? "#eee" : "white",
      margin: login ? "5px 0" : "0",
      outline: "none",
      // borderColor: "transparent",
      padding: "0 0 0 10px",
      color: "#898989",
    },
    fieldset: {
      border: "none",
    },
    "@media (max-width: 900px)": {},
  })
);

interface MyLabelProps {
  color?: string;
}

export const MyLabel = styled(Typography)<MyLabelProps>(({ color, theme }) => ({
  color: color === "dark" ? theme.palette.common.black : color,
  fontSize: "1rem",

  "@media (max-width: 900px)": {},
}));
