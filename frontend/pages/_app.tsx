import * as React from "react";
import type { AppProps } from "next/app";
import Head from "next/head";
import { CacheProvider, EmotionCache } from "@emotion/react";
import { ThemeProvider, CssBaseline, createTheme } from "@mui/material";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

import createEmotionCache from "../utility/createEmotionCache";
import lightThemeOptions from "../styles/theme/lightThemeOptions";
import "../styles/globals.css";
import { NavBar } from "../components/navbar";
import { RecoilRoot } from "recoil";
import {
  useSsrComplectedState,
  useToken,
} from "../src/atoms/accounts/accountsAtom";
import Router from "next/router";
import { useLoading } from "../src/hooks";
import { useLoginRequired } from "../src/hooks/accounts/accountsHooks";
interface MyAppProps extends AppProps {
  emotionCache?: EmotionCache;
}

const clientSideEmotionCache = createEmotionCache();

const MyApp: React.FunctionComponent<MyAppProps> = (props) => {
  return (
    <RecoilRoot>
      <RecoilRenderer {...props} />
    </RecoilRoot>
  );
};
const RecoilRenderer: React.FunctionComponent<MyAppProps> = (props) => {
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;
  const ssrCompleted = useSsrComplectedState();
  const required = ["admin", "info"];
  useLoginRequired(required);
  if (!ssrCompleted) {
    return <div>로딩중!</div>;
  }
  return (
    <CacheProvider value={emotionCache}>
      <Head>
        <meta name="viewport" content="initial-scale=1, width=device-width" />
        <title>Mussage</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <ThemeProvider theme={lightThemeOptions}>
        <CssBaseline />
        <NavBar />
        <Component {...pageProps} />
      </ThemeProvider>
    </CacheProvider>
  );
};

export default MyApp;
