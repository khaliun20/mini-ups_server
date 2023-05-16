import React, { useState } from 'react';
import DisplayQuoteComponent from './DisplayQuoteComponent';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from "../security/AuthContext"
import { Card, CardBody, CardTitle, CardSubtitle, Button } from 'reactstrap';

function AvailableQuotesComponent({ basicRate }) {
    const [selectedOption, setSelectedOption] = useState(null);
    const [showQuote, setShowQuote] = useState(false);

    const handleClick = () => {
        setShowQuote(true);
    }

    const authContext = useAuth()
    const isAuthenticated = authContext.isAuthenticated
    
    const navigate = useNavigate()
    // Make sure basicRate is defined before calculating shipping options
    if (!basicRate) {
        return <div>Loading...</div>;
    }

    // Calculate three different shipping options using the basic rate
    const upsNextDayAirSaver = basicRate * 1.5;
    const upsGround = basicRate;
    const upsNextDayAir = basicRate * 3;

    // Calculate the expected delivery dates for each option
    const upsNextDayAirSaverDeliveryDate = new Date(Date.now() + 24 * 60 * 60 * 1000);
    const upsGroundDeliveryDate = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);
    const upsNextDayAirDeliveryDate = new Date(Date.now() + 24 * 60 * 60 * 1000);

    // Format the delivery dates as strings
    const upsNextDayAirSaverDeliveryDateString = upsNextDayAirSaverDeliveryDate.toLocaleDateString();
    const upsGroundDeliveryDateString = upsGroundDeliveryDate.toLocaleDateString();
    const upsNextDayAirDeliveryDateString = upsNextDayAirDeliveryDate.toLocaleDateString();

    return (
        <div>
         {!showQuote &&
        <div className="d-flex flex-wrap justify-content-center">
            <Card className="mx-2 my-4" style={{ minWidth: '300px', maxWidth: '400px' }}>
                <CardBody>
                    <CardTitle>Our Recommendation</CardTitle>
                    <CardSubtitle>UPS Next Day Air Saver</CardSubtitle>
                    <p className="mt-3 mb-2">Expected delivery:</p>
                    <p>{upsNextDayAirSaverDeliveryDateString}</p>
                    <p className="mt-3 mb-2">Price:</p>
                    <p>{upsNextDayAirSaver ? `$${upsNextDayAirSaver.toFixed(2)}` : ''}</p>
                    <Button onClick={() => setSelectedOption('upsNextDayAirSaver')} disabled={!upsNextDayAirSaver}>Select</Button>
                </CardBody>
            </Card>

            <Card className="mx-2 my-4" style={{ minWidth: '300px', maxWidth: '400px' }}>
                <CardBody>
                    <CardTitle>Lowest Cost</CardTitle>
                    <CardSubtitle>UPS Ground</CardSubtitle>
                    <p className="mt-3 mb-2">Expected delivery:</p>
                    <p>{upsGroundDeliveryDateString}</p>
                    <p className="mt-3 mb-2">Price:</p>
                    <p>{upsGround ? `$${upsGround.toFixed(2)}` : ''}</p>
                    <Button onClick={() => setSelectedOption('upsGround')} disabled={!upsGround}>Select</Button>
                </CardBody>
            </Card>

            <Card className="mx-2 my-4" style={{ minWidth: '300px', maxWidth: '400px' }}>
                <CardBody>
                    <CardTitle>Fastest Way</CardTitle>
                    <CardSubtitle>UPS Next Day Air</CardSubtitle>
                    <p className="mt-3 mb-2">Expected delivery:</p>
                    <p>{upsNextDayAirDeliveryDateString}</p>
                    <p className="mt-3 mb-2">Price:</p>
                    <p>{upsNextDayAir ? `$${upsNextDayAir.toFixed(2)}` : ''}</p>
                    <Button onClick={() => setSelectedOption('upsNextDayAir')} disabled={!upsNextDayAir}>Select</Button>
                </CardBody>
            </Card>
            </div>
        }

        <div>
        {!showQuote && <Button onClick={handleClick}>Back</Button>}
        
        {showQuote && <DisplayQuoteComponent />}
        {!showQuote && 
        <Button onClick={() => {
            if (selectedOption) {
                // Navigate to shipping form
                navigate(`/ship`)
            } else {
                // Show error message or disable button
                
            }
        }} disabled={!selectedOption || !isAuthenticated}>Start Shipping</Button>}
        { !isAuthenticated && <p>Please first log in to start shipping!</p>}
    </div>
    </div>
    )
}

export default AvailableQuotesComponent
