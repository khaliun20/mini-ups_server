import React from 'react';
import { createContext, useContext, useState } from "react";
import { useEffect } from 'react';

export const AuthContext = createContext()

export const useAuth = () => useContext(AuthContext)


export default function AuthProvider({ children }){
    const [ upsUser, setUpsUser ] = useState(null)
    const [ isAuthenticated, setIsAuthenticated ] = useState(false)

    function logout(){
        setIsAuthenticated(false)
        setUpsUser(null);
        localStorage.clear();
    }

    useEffect(() => {
        const loggedInUser = localStorage.getItem("user");
        console.log("loggedin")
        console.log(loggedInUser)
        if (loggedInUser) {
            // const foundUser = JSON.parse(loggedInUser);
            // authContext.setUpsUsr(foundUser);
            setUpsUser(loggedInUser)
            setIsAuthenticated(true)
        }
    }, []);
    

    return (
        <AuthContext.Provider value={ {isAuthenticated, logout, upsUser, setUpsUser, setIsAuthenticated } }>
            { children }
        </AuthContext.Provider>
    )
}

