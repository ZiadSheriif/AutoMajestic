import { baseAPI } from "./axios.api";

export function getNfa(regex: string) {
  return baseAPI({
    method: "GET",
    url: `/compile/nfa`,
    requestConfig: {
      params: { regex: regex },
      headers: {
        "Content-Language": "en-US",
      },
    },
  });
}
