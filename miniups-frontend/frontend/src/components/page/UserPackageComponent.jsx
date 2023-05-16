import React from 'react';
import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useAuth } from "../security/AuthContext"
import { retrieveAllPackagesForUser, addPackageForUser } from "../api/trackingApiService"
import PackageDisplayComponent from "./PackageDisplayComponent"
import AddNewPackage from "./AddNewPackage"
import "../styles/Display.css"
import { Alert } from 'reactstrap';


function UserPackageComponent(){
    const { username } = useParams()

    const [ allPackages, setAllPackages ] = useState([])
    const [ addNewPack, setAddNewPack ] = useState(false)
    const [ errorMessage, setErrorMessage ] = useState(null)

    const authContext = useAuth()
    const isAuthenticated = authContext.isAuthenticated

    useEffect( () => refreshPackages(), [] )

    function refreshPackages(){
        retrieveAllPackagesForUser(username)
        .then(response => {
            console.log(response)
            setAllPackages(response.data)
        })
        .catch(error => console.log(error))
    }

    function addNewPackage(){
        setAddNewPack(true)
    }

    function handleAddNewPackage(event, trackingNum) {
        event.preventDefault();
        
        addPackageForUser(username.toString(), trackingNum)
            .then(response => {
                console.log(response.data);
                setAddNewPack(false);
                refreshPackages()
        })
        .catch(error =>{ 
            console.error(error)
            setErrorMessage("Cannot find this package. Please try again")
        });
    }

    return(
        <div className="container" style={{ marginTop: '20px', overflow: "scroll" }}>
            <h1>Your Package: </h1>
            {allPackages && <PackageDisplayComponent packageInfo={ allPackages } />}
            {isAuthenticated && 
                <div  style={{ marginBottom: '10px', overflow: "scroll" }}>
                    <h2>Didn't Find Your Packages? Add Here: </h2>
                    <div className="btn btn-success m-5" 
                        onClick={ addNewPackage } 
                        style={{ backgroundColor: '#7C9070', fontSize: '1.5rem' }} >
                        Add New Package
                    </div>
                </div>
            }
            {addNewPack &&  
                <div>
                    { errorMessage && <Alert color="danger">{errorMessage}</Alert> }
                    <AddNewPackage onAddNewPackage={handleAddNewPackage} onCancel={() => setAddNewPack(false)} />
                </div>
            }
        </div>
    )
}

export default UserPackageComponent