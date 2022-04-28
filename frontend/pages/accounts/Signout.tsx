import Router from "next/router";
import React, { useEffect } from "react";
import { useToken } from "../../src/atoms/accounts/accountsAtom";
import { deleteCookie } from "../../src/functions/accounts/cookies";
import { TokenType } from "../../src/types/accounts/accountsTypes";

interface SignoutProps {}
const Signout: React.FunctionComponent<SignoutProps> = (props) => {
  const [token, setToken] = useToken();
  useEffect(() => {
    const emptyToken: TokenType = {
      id: 0,
      expired_in: "",
      user: 0,
      token: "",
    };
    deleteCookie("token");
    setToken(emptyToken);
  }, []);
  useEffect(() => {
    Router.push("/");
  }, [token]);
  return <div>사인아웃</div>;
};
export default Signout;
