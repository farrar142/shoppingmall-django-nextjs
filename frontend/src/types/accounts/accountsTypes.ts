
export interface TokenType { 
    expired_in: string
    id: number
    token: string
    user:number
}
  
export interface ShopType {
  name: string;
}
export interface EmptyType {}
export interface userInfoType {
  username: string;
  email: string;
  shop: Array<ShopType | EmptyType>;
}