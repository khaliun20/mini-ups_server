import React from 'react';
import { useNavigate, useParams} from "react-router-dom"
import { updateLocationForPackage } from "../api/trackingApiService"
import { useState } from "react"
import { useAuth } from "../security/AuthContext"

function UpdateAddressComponent(){

    const { trackingNum } = useParams();
    const navigate = useNavigate();
    const [x, setX] = useState("");
    const [y, setY] = useState("");


    const authContext = useAuth()
    const isAuthenticated = authContext.isAuthenticated
    const username = authContext.upsUser

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await updateLocationForPackage(trackingNum, x, y);
            if(isAuthenticated){
                navigate(`/home/${username}`);
            }else{
                navigate(`/`);
            }
            
        } catch (error) {
            console.error(error);
        }
        
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="x">Change X</label>
                <input
                    type="text"
                    id="x"
                    name="x"
                    value={x}
                    onChange={(event) => setX(event.target.value)}
                />
            </div>
            <div>
                <label htmlFor="y">Change Y</label>
                <input
                    type="text"
                    id="y"
                    name="y"
                    value={y}
                    onChange={(event) => setY(event.target.value)}
                />
            </div>
            <button type="submit">Update</button>
            </form>
    );
}

export default UpdateAddressComponent