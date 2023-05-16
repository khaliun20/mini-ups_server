import { apiMiniUPSClient } from "./apiClient";

export const createNewUser 
    = (username, password, state) => apiMiniUPSClient.post(`/api/users`, {username, password, state})

export const getUser
    = (username) => apiMiniUPSClient.get(`/api/users/${username}`)

export const executeJwtAuthenticationService
    = (username, password) => 
    apiMiniUPSClient.post(`/authenticate`, {username,password} )