import { Box, Button, Typography } from "@mui/material";
import { useCompile } from "../../../presenter/useCompile";
import TextField from "../../components/TextField/TextField";
import {
  ButtonsContainer,
  Container,
  ImageContainer,
  InputContainer,
} from "./Home.styled";
import toast, { Toaster } from "react-hot-toast";
import { useState, useEffect } from "react";

const Home = () => {
  const [regex, setRegex] = useState("");
  const [type, setType] = useState("NFA");
  const [image, setImage] = useState();

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
    if (type == "NFA") {
      if (data_nfa) {
        setImage(data_nfa);
      }
    } else if (type == "DFA") {
      if (data_dfa) {
        setImage(data_dfa);
      }
    } else if (type == "MIN-DFA") {
      if (data_min_dfa) {
        setImage(data_min_dfa);
      }
    }
  }, [data_nfa, data_dfa, data_min_dfa]);

  useEffect(() => {
    if (isError_nfa) {
      toast.error("This Regex is invalid");
    }
  }, [isError_nfa]);

  const handleGetNfa = () => {
    setType("NFA");
    nfa(regex);
  };

  const handleGetDfa = () => {
    setType("DFA");
    dfa(regex);
  };

  const handleGetMinDfa = () => {
    setType("MIN-DFA");
    minDfa(regex);
  };

  return (
    <Container>
      <InputContainer>
        <TextField
          value={regex}
          setValue={setRegex}
          label="Regex:"
          placeHolder={""}
        />
        <ButtonsContainer>
          <Button onClick={handleGetNfa} disabled={!regex}>
            Get NFA
          </Button>
          <Button onClick={handleGetDfa} disabled={!regex}>
            Get DFA
          </Button>
          <Button onClick={handleGetMinDfa} disabled={!regex}>
            Get Min-DFA
          </Button>
        </ButtonsContainer>
      </InputContainer>
      <ImageContainer>
        {image && (
          <Box>
            <Typography>{type}</Typography>
            <img src={"data:image/png;base64," + image.image} />
          </Box>
        )}
      </ImageContainer>
    </Container>
  );
};

export default Home;
