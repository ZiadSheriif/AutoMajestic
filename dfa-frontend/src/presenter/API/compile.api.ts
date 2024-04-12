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

export function getDfa(regex: string) {
  return baseAPI({
    method: "GET",
    url: `/compile/dfa`,
    requestConfig: {
      params: { regex: regex },
      headers: {
        "Content-Language": "en-US",
      },
    },
  });
}

export function getMinDfa(regex: string) {
  return baseAPI({
    method: "GET",
    url: `/compile/min-dfa`,
    requestConfig: {
      params: { regex: regex },
      headers: {
        "Content-Language": "en-US",
      },
    },
  });
}
