import { apiMiniUPSClient } from "./apiClient";


export const getAllShippingLabelFromUser
    = (username) => apiMiniUPSClient.get(`/labels/${username}`)

export const getClosestUpsLocation
    = (x, y) => apiMiniUPSClient.post(`/ups-location/${x}/${y}`)