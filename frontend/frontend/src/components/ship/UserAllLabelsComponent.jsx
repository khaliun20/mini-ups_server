import React from 'react';
import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useAuth } from "../security/AuthContext"
import { getAllShippingLabelFromUser } from "../api/extraCredit.js"
import "../styles/Display.css"
import AllShippingLabelComponent from './AllShippingLabelComponent';


function UserAllLabelComponent(){
    const { username } = useParams()

    const [ allLabels, setAllLabels ] = useState([])

    const authContext = useAuth()
    const isAuthenticated = authContext.isAuthenticated

    useEffect( () => refreshShippingLabel(), [] )

    function refreshShippingLabel(){
        getAllShippingLabelFromUser(username)
        .then(response => {
            console.log(response)
            setAllLabels(response.data)
        })
        .catch(error => console.log(error))
    }

    return(
        <div className="container" style={{ marginTop: '20px', overflow: "scroll" }}>
            <h1>All Your Created ShippingLabels: </h1>
            {isAuthenticated && allLabels && <AllShippingLabelComponent shippingLabelInfo={ allLabels } />}
        </div>
    )
}

export default UserAllLabelComponent