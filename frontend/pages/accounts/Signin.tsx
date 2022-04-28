import React, { useEffect, useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import lightThemeOptions from "../../styles/theme/lightThemeOptions";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment } from "@fortawesome/free-solid-svg-icons";
import { ThemeProvider } from "@mui/material";
import axios from "axios";
import Router from "next/router";
import { useBrowserId, useToken } from "../../src/atoms/accounts/accountsAtom";
import { TokenType } from "../../src/types/accounts/accountsTypes";
import { SetterOrUpdater } from "recoil";
import { setCookie } from "../../src/functions/accounts/cookies";

function Copyright(props: any) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

export default function SignIn() {
  const [kakaoWs, setKakaoWs] = useState<null | WebSocket>(null);
  const browserId = useBrowserId();
  const [token, setToken] = useToken();
  useEffect(() => {
    setKakaoWs(
      new WebSocket(
        "wss://shopbackend.honeycombpizza.link/ws/kakao/" + browserId + "/"
      )
    );
  }, []);
  if (token.user) {
    Router.push("/");
  }
  if (kakaoWs) {
    kakaoWs.onopen = (e) => {
      console.log("연결되었어요!");
    };
    kakaoWs.onmessage = (e: MessageEvent<any>) => {
      const res = JSON.parse(e.data);
      const token: TokenType = res.token;
      setCookie("token", token.token);
      setToken(token);
    };
    kakaoWs.onclose = (e) => {
      console.log("연결해제됨");
    };
  }
  const kakaoLogin = async (event: React.MouseEvent<HTMLElement>) => {
    const result = await axios.get(
      "https://shopbackend.honeycombpizza.link/api/accounts/kakao_login?browser_id=" +
        browserId
    );
    if (result.data.url) {
      window.open(result.data.url);
    }
  };
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      email: data.get("email"),
      password: data.get("password"),
    });
  };

  return (
    <ThemeProvider theme={lightThemeOptions}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>

            <Button
              color="kakao"
              fullWidth
              variant="contained"
              size="small"
              sx={{ mt: 3, mb: 2 }}
              onClick={kakaoLogin}
            >
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-around",
                  width: "100%",
                  alignItems: "center",
                }}
              >
                <FontAwesomeIcon
                  style={{ height: "30px" }}
                  color="black"
                  icon={faComment}
                />
                <Typography color="common.black">Login with Kakao</Typography>
                <Box />
              </Box>
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="#" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
    </ThemeProvider>
  );
}
