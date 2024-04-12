import { Button } from "@mui/material";
import { useCompile } from "../../../presenter/useCompile";
import TextField from "../../components/TextField/TextField";
import { Container, ImageContainer, InputContainer } from "./Home.styled";

import { useState, useEffect } from "react";

const Home = () => {
  const [regex, setRegex] = useState("");

  const {
    nfa,
    data_nfa,
    isLoading_nfa,
    isSuccess_nfa,
    isError_nfa,
    error_nfa,
  } = useCompile();

  useEffect(() => {
    if (data_nfa) {
      console.log(data_nfa);
    }
  }, [data_nfa]);

  const handleGetNfa = () => {
    nfa(regex);
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
        <Button
          onClick={handleGetNfa}
          sx={{ float: "right" }}
          disabled={!regex}
        >
          Get Nfa
        </Button>
      </InputContainer>
      <ImageContainer></ImageContainer>
    </Container>
  );
};

export default Home;
