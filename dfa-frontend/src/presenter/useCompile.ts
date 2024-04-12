import { getNfa, getDfa, getMinDfa } from "./API/compile.api";
import useAPI from "./services/useAPI.service";
export function useCompile() {
  const {
    data: data_nfa,
    isLoading: isLoading_nfa,
    isSuccess: isSuccess_nfa,
    isError: isError_nfa,
    error: error_nfa,
    runQuery: runQuery_nfa,
  } = useAPI();

  const nfa = (regex: string) => {
    runQuery_nfa(() => getNfa(regex));
  };


  const {
    data: data_dfa,
    isLoading: isLoading_dfa,
    isSuccess: isSuccess_dfa,
    isError: isError_dfa,
    error: error_dfa,
    runQuery: runQuery_dfa,
  } = useAPI();

  const dfa = (regex: string) => {
    runQuery_dfa(() => getDfa(regex));
  };


  const {
    data: data_min_dfa,
    isLoading: isLoading_min_dfa,
    isSuccess: isSuccess_min_dfa,
    isError: isError_min_dfa,
    error: error_min_dfa,
    runQuery: runQuery_minDfa,
  } = useAPI();

  const minDfa = (regex: string) => {
    runQuery_minDfa(() => getMinDfa(regex));
  };

  return {
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
  };
}
