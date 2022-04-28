import {
  Box,
  Button,
  Container,
  FormControl,
  IconButton,
  Paper,
  Stack,
  styled,
  TextField,
  Typography,
} from "@mui/material";
import { NextPage } from "next";
import React, {
  ChangeEventHandler,
  FunctionComponent,
  InputHTMLAttributes,
  useRef,
  useState,
} from "react";
import ImageUploader from "../components/ImageUploader";
import { useUserInfo } from "../src/functions/accounts";
import { useLoginRequired } from "../src/hooks/accounts/accountsHooks";
import PhotoCamera from "@mui/icons-material/PhotoCamera";
import { ImageListType } from "react-image-uploading";
import { useToken } from "../src/atoms/accounts/accountsAtom";
import { useLoading } from "../src/hooks";
import axios from "axios";
import { setCookie } from "../src/functions/accounts/cookies";
import Image from "next/image";
interface AdminProps {}
const AdminPage: NextPage<AdminProps> = (props) => {
  const [token, setToken] = useToken();
  const isLoading = useLoading();
  const userInfo = useUserInfo(token);

  if (!isLoading) {
    return <div></div>;
  } else if (userInfo) {
    if (userInfo.shop.length == 0) {
      return <RegisterShop />;
    }
  }
  return (
    <Container>
      <Paper>
        <Typography>가게 보기</Typography>
      </Paper>
    </Container>
  );
};
const RegisterShop: FunctionComponent = () => {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | ArrayBuffer | null>(null);
  const inputRef = useRef(null);

  const submitHandler = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (image !== null) {
      const filesEl: HTMLInputElement | null =
        window.document.querySelector("#multiFiles");
      const form = new FormData(e.currentTarget);
      if (filesEl?.files) {
        form.append("file", filesEl.files[0]);
      }
      const url = "/api/accounts/test";
      const method = "post";
      fetch(url, {
        method: method,
        headers: {},
        body: form,
      });
    }
  };
  const handleFileSelected = (e: React.ChangeEvent<HTMLInputElement>): void => {
    if (e.target.files) {
      const files = e.target.files;
      setImage(files[0]);
      let reader = new FileReader();
      let file = files[0];
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  return (
    <Container>
      <Paper>
        <Typography>가게 등록</Typography>
        <Container sx={{ display: "flex", justifyContent: "center" }}>
          <form
            onSubmit={submitHandler}
            method="post"
            encType="multipart/form-data"
          >
            <Stack spacing={1}>
              <TextField
                label="매장이름"
                name="name"
                autoComplete="off"
              ></TextField>
              <TextField
                label="매장사이트"
                name="siteUrl"
                autoComplete="off"
              ></TextField>
              <TextField
                label="매장이메일"
                name="email"
                autoComplete="off"
              ></TextField>
              <TextField
                label="설명"
                name="desc"
                autoComplete="off"
              ></TextField>
              {typeof preview == "string" ? (
                <Image src={preview} alt="" height="200%" width="100%"></Image>
              ) : null}
              <input
                id="multiFiles"
                ref={inputRef}
                type="file"
                name="file"
                onChange={handleFileSelected}
              />
            </Stack>
            <input type="submit" />
          </form>
        </Container>
      </Paper>
    </Container>
  );
};
export default AdminPage;
