import { Box, Paper, Tab, Tabs, Typography } from "@mui/material";
import type { NextPage } from "next";
import { useState } from "react";
import { useToken } from "../../src/atoms/accounts/accountsAtom";
import { useUserInfo } from "../../src/functions/accounts";
import { useLoading } from "../../src/hooks";
import { useLoginRequired } from "../../src/hooks/accounts/accountsHooks";
import {
  TokenType,
  userInfoType,
} from "../../src/types/accounts/accountsTypes";

interface infoProps {
  token: TokenType;
}
function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}
const Info: NextPage<infoProps> = (props) => {
  const [page, setPage] = useState<number>(0);
  const [token, setToken] = useToken();
  const isLoading = useLoading();
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setPage(newValue);
  };
  const userInfo = useUserInfo(token);
  if (!isLoading) {
    return <div>로딩중</div>;
  }
  if (userInfo?.username) {
    return (
      <Paper>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={page}
            onChange={handleChange}
            aria-label="basic tabs example"
          >
            <Tab label="주문 배송" {...a11yProps(0)} />
            <Tab label="포인트" {...a11yProps(1)} />
            <Tab label="개인 정보" {...a11yProps(2)} />
          </Tabs>
        </Box>
        <OrderAndDelivery value={page} index={0} />
        <PointPage value={page} index={1} />
        <MyPage value={page} userInfo={userInfo} index={2} />
      </Paper>
    );
  } else {
    return <div>로딩중</div>;
  }
};
interface TabPanelProps {
  children?: React.ReactNode;
  userInfo?: userInfoType | null;
  index: number;
  value: number;
}

const OrderAndDelivery = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;
  return (
    <Box
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value}번페이지
    </Box>
  );
};
const PointPage = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;
  return (
    <Box
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value}번페이지
    </Box>
  );
};
const MyPage: React.FunctionComponent<TabPanelProps> = (props) => {
  const { children, value, index, userInfo, ...other } = props;
  return (
    <Box
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      <Typography>{userInfo?.username}</Typography>
      <Typography>{userInfo?.email}</Typography>
    </Box>
  );
};

export default Info;
