import { getNfa } from "./API/compile.api";
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

  return {
    nfa,
    data_nfa,
    isLoading_nfa,
    isSuccess_nfa,
    isError_nfa,
    error_nfa,
  };
}
