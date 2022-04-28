import { useLoading } from './../index';
import { useSsrComplectedState } from './../../atoms/accounts/accountsAtom';
import  axios  from 'axios';
import { TokenType } from './../../types/accounts/accountsTypes';
import  Router  from 'next/router';
import { useEffect, useState } from "react"
import { useToken } from "../../atoms/accounts/accountsAtom"
import { deleteCookie, getCookie } from '../../functions/accounts/cookies';

export const useLoginRequired = (paths:string[]): void => { 
    
  const [token, setToken] = useToken();
    const ssrCompleted = useSsrComplectedState();
    const isLoading = useLoading()
    useEffect(() => { 
        const fullPath = Router.pathname
        const isIncluded = paths.filter(res => fullPath.includes(res)).length >= 1
        const check_login = async () => {
            // const token = getCookie("token")
            const res = await axios.post("/api/accounts/check_login/", { token: token.token })
            if (res.data.result === false || !token.token) {
                deleteCookie("token")
                Router.push('/accounts/Signin')
            } else { 
            }
        }
        if (ssrCompleted&&isLoading&&isIncluded) {
            check_login()
        } else { 
            
    console.log("로딩중!");
        }
    }, [token,paths,ssrCompleted])
    
}