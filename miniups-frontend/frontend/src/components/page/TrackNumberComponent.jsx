import React from 'react';
import { useState } from "react";
import { retrievePackageForTrackingNum, getTruckFromTrackingNum } from "../api/trackingApiService"
import '../styles/LocationDisplayComponent.css'
import PackageDisplayComponent from "./PackageDisplayComponent";
import LocationDisplayComponent from "./LocationDisplayComponent";
import "../styles/Display.css"
import { Form, FormGroup, Label, Input, Button } from "reactstrap";
import AudioPlayer from './AudioPlayer';
import audio from './music.mp3';


function TrackNumberComponent() {
    const [trackingNum, setTrackingNum] = useState("");
    const [packageInfo, setPackageInfo] = useState(null);
    const [findPackageMsg, setFindPackageMsg] = useState(null); 
    const [truck, setTruck] = useState(null);

    // const navigate = useNavigate()


    const handleTrackingNumChange = (event) => {
        setTrackingNum(event.target.value);
    };  
    
    const handleFormSubmit = (event) => {
        event.preventDefault();
        retrievePackageForTrackingNum(trackingNum)
            .then((response) => {
                setPackageInfo(response.data);
                if(response.data !== null){
                    setFindPackageMsg("Package found");
                }

                
                getTruckFromTrackingNum(trackingNum)
                    .then((statusResponse) => {
                        setTruck(statusResponse.data);
                    })
                    .catch((error) => {
                        console.error(error);
                    });
        })
        .catch((error) => {
            if (error.response) {
                if(error.response.status === 404)
                    setFindPackageMsg("Package not found");
                if(error.response.status === 400)
                    setFindPackageMsg("Please only enter number");
                // setPackageInfo([]);
                console.log(error);
            } else {
                console.log(error);
            }
        });
    };  
    return (
        <div style={{ overflow: "scroll" }}>
        <h1 >Track Your Package</h1>
        <AudioPlayer source={audio} />

        <Form onSubmit={handleFormSubmit}>
            <FormGroup>
            <Label for="trackingNum" style={{ fontFamily: "Karla", fontSize: "30px" }}>Enter your tracking number:</Label>
            <Input type="text" name="trackingNum" id="trackingNum" value={trackingNum} onChange={handleTrackingNumChange} style={{ width: '60%', margin: '0 auto', textAlign: 'center' }} />
            </FormGroup>
            <Button type="submit" >Track Package</Button>
        </Form>
    
        {findPackageMsg !== "Package found" && <div>{findPackageMsg}</div>}
        {findPackageMsg === "Package found" && (
            <div>
            <PackageDisplayComponent packageInfo={packageInfo} />
            {packageInfo[0].state !== "delivered" && (
                <div>
                <h2>Your Current Package Location: </h2>
                <div className="location-display">
                    {truck && <LocationDisplayComponent x={truck.x} y={truck.y} />}
                </div>
                </div>
            )}
            </div>
        )}
        </div>
    );

    // return (
    //     <div style={{ overflow: 'scroll'}}>
    //         <h1>Track Your Package</h1>
    //         <form onSubmit={handleFormSubmit}>
    //             <div>
    //                 <label>Enter your tracking number:</label>
    //                 <input type="text" value={trackingNum} onChange={handleTrackingNumChange} />
    //                 <button type="submit">Track Package</button>
    //             </div>
    //         </form>

    //         {findPackageMsg !== "Package found" && <div>{findPackageMsg}</div>}
    //         {findPackageMsg === "Package found" &&
    //             <div>
    //                 <PackageDisplayComponent packageInfo={ packageInfo } />
    //                 { packageInfo[0].state !== 'delivered' && 
    //                     <div>
    //                         <h2>Your Current Package Location: </h2>
    //                         <div className='location-display'>
    //                         {truck  && <LocationDisplayComponent x={ truck.x } y={ truck.y } />}
    //                         </div>
    //                     </div>
    //                 }

    //             </div>

    //         }
    //     </div>
    // );
}

export default TrackNumberComponent;
