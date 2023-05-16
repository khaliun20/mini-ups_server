import { apiMiniUPSClient } from "./apiClient";


export const retrievePackageForTrackingNum = 
    (trackingNum) => apiMiniUPSClient.get(`/packages/${trackingNum}`)

export const retrieveAllItemsInPackage = 
    (trackingNum) => apiMiniUPSClient.get(`/${trackingNum}/items`)

export const updateLocationForPackage = 
    (trackingNum, x, y) => apiMiniUPSClient.post(`/location/${trackingNum}/${x}/${y}`)


export const getTruckFromTrackingNum = 
    (trackingNum) => apiMiniUPSClient.get(`/trucks/${trackingNum}`)


export const retrieveAllPackagesForUser = 
    (username) => apiMiniUPSClient.get(`/${username}/packages`)


export const addPackageForUser = 
    (username, trackingNum) => apiMiniUPSClient.post(`/${username}/packages/${trackingNum}`)








export const deletePackageForUser = 
    (username, id) => apiMiniUPSClient.delete(`/users/${username}/todos/${id}`)


export const retrivePackageForUser = 
    (username, id) => apiMiniUPSClient.get(`/users/${username}/todos/${id}`)

export const updatePackageForUser = 
    (username, id, todo) => apiMiniUPSClient.put(`/users/${username}/todos/${id}`, todo)