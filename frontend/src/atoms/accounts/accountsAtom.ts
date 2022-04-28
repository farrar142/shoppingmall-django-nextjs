import { useEffect } from 'react';
import { TokenType } from './../../types/accounts/accountsTypes';

import { atom, AtomEffect, atomFamily, SetterOrUpdater, useRecoilState, useSetRecoilState } from "recoil";
import { recoilPersist } from "recoil-persist";
import { uuid4 } from "../../functions/accounts/uuid4";

const { persistAtom } = recoilPersist();
const ssrCompletedState = atom({
  key: "SsrCompleted",
  default: false,
});

export const useSsrComplectedState = ():boolean => {
  const [ssrCompleted, setSsrCompleted] = useRecoilState<boolean>(ssrCompletedState);
  
    useEffect(() => {
      if (!ssrCompleted)setSsrCompleted(true)
    }, [ssrCompleted]);
  return ssrCompleted
};

export const persistAtomEffect = <T>(param: Parameters<AtomEffect<T>>[0]) => {
    param.getPromise(ssrCompletedState).then(() => persistAtom(param))
}
const browserIdAtom = atom<string>({
  key: "browserId",
  default: btoa(uuid4()),
  effects_UNSTABLE:[persistAtomEffect]
})
const tokenAtom = atom<TokenType>({
  key: "tokenAtom",
  default: {expired_in:"",id:0,token:"",user:0},
  effects_UNSTABLE:[persistAtomEffect]
})
type tokenReturn = [TokenType,(e:TokenType)=>void]
export const useToken = ():tokenReturn => { 
  const [getter, setter] = useRecoilState<TokenType>(tokenAtom)
  const handler = (e: TokenType) => { 
    setter(e)
  }
  return [getter,handler]
}
export const useBrowserId = () => { 
  const [getter, setter] = useRecoilState<string>(browserIdAtom)
  const handler = (e: string) => { 
    setter(e)
  }
  return getter
}