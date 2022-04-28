import { TokenType } from './../../types/accounts/accountsTypes';
import axios from "axios";
import { useEffect, useState } from "react";
import { userInfoType } from "../../types/accounts/accountsTypes";
import { getCookie } from "./cookies";
type useUserInfoReturn=userInfoType|null

export function useUserInfo(token:TokenType):useUserInfoReturn{ 
    const [userInfo, setUserInfo] = useState<userInfoType | null>(null);
    useEffect(() => {
      const ue = async () => {
        if (token.token) {
          const info = await axios.post("/api/accounts/info", { token: token.token });
          const _userInfo: userInfoType = info.data;
          setUserInfo(_userInfo);
        }
      };
      ue();
    }, [token]);
    return userInfo
}