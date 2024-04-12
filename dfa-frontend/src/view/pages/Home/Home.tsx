import { Box, Button, Typography } from "@mui/material";
import { useCompile } from "../../../presenter/useCompile";
import TextField from "../../components/TextField/TextField";
import {
  ButtonsContainer,
  Container,
  ImageContainer,
  InputContainer,
  Left,
} from "./Home.styled";
import toast from "react-hot-toast";
import { useState, useEffect } from "react";
import CircularProgress from "@mui/material/CircularProgress";

const Home = () => {
  const [regex, setRegex] = useState("");
  const [type, setType] = useState("");
  const [image, setImage] = useState();
  const [enter, setEnter] = useState(false);

  const {
    nfa,
    data_nfa,
    isLoading_nfa,
    isSuccess_nfa,
    isError_nfa,
    error_nfa,
    dfa,
    data_dfa,
    isLoading_dfa,
    isSuccess_dfa,
    isError_dfa,
    error_dfa,
    minDfa,
    data_min_dfa,
    isLoading_min_dfa,
    isSuccess_min_dfa,
    isError_min_dfa,
    error_min_dfa,
  } = useCompile();

  useEffect(() => {
    if (!isLoading_nfa && !isLoading_dfa && !isLoading_min_dfa) {
      if (type == "NFA") {
        if (data_nfa) {
          setImage(data_nfa);
        } else if (isError_nfa) {
          toast.error("This Regex is invalid");
        }
      } else if (type == "DFA") {
        if (data_dfa) {
          setImage(data_dfa);
        } else if (isError_dfa) {
          toast.error("This Regex is invalid");
        }
      } else if (type == "MIN-DFA") {
        if (data_min_dfa) {
          setImage(data_min_dfa);
        } else if (isError_min_dfa) {
          toast.error("This Regex is invalid");
        }
      }
    }
  }, [
    data_nfa,
    data_dfa,
    data_min_dfa,
    type,
    enter,
    isLoading_nfa,
    isLoading_dfa,
    isLoading_min_dfa,
    isError_nfa,
    isError_dfa,
    isError_min_dfa,
  ]);

  const handleGetNfa = () => {
    setType("NFA");
    setEnter(!enter);
    nfa(regex);
  };

  const handleGetDfa = () => {
    setType("DFA");
    setEnter(!enter);
    dfa(regex);
  };

  const handleGetMinDfa = () => {
    setType("MIN-DFA");
    setEnter(!enter);
    minDfa(regex);
  };

  return (
    <Container>
      <Left>
        <Typography
          sx={{ fontSize: "1rem", marginBottom: "5px", color: "white" }}
        >
          AutoMajestic
        </Typography>
        <InputContainer>
          <TextField
            value={regex}
            setValue={setRegex}
            label="Regex:"
            placeHolder={""}
          />
          <ButtonsContainer>
            <Button
              onClick={handleGetNfa}
              disabled={!regex}
              sx={{
                color: "#F2613F",
                "&:disabled": {
                  color: "gray",
                },
              }}
            >
              Get NFA
            </Button>
            <Button
              onClick={handleGetDfa}
              disabled={!regex}
              sx={{
                color: "#F2613F",
                "&:disabled": {
                  color: "gray",
                },
              }}
            >
              Get DFA
            </Button>
            <Button
              onClick={handleGetMinDfa}
              disabled={!regex}
              sx={{
                color: "#F2613F",
                "&:disabled": {
                  color: "gray",
                },
              }}
            >
              Get Min-DFA
            </Button>
          </ButtonsContainer>
        </InputContainer>
      </Left>
      <ImageContainer>
        {image && (
          <Box>
            {isLoading_nfa || isLoading_dfa || isLoading_min_dfa ? (
              <CircularProgress />
            ) : (
              <>
                <Typography
                  sx={{
                    fontSize: "1.6rem",
                    marginBottom: "5px",
                    color: "white",
                  }}
                >
                  {type}
                </Typography>
                <img src={"data:image/png;base64," + image.image} />
              </>
            )}
          </Box>
        )}
      </ImageContainer>
    </Container>
  );
};

export default Home;
