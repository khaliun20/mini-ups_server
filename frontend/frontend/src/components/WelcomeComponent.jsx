import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import TrackNumberComponent from "./page/TrackNumberComponent";
import { Container} from "reactstrap";
import "./styles/Display.css"
import QuoteComponent from './quote/QuoteComponent';
import { useAuth } from "./security/AuthContext"


function WelcomeComponent() {
    const [activeComponent, setActiveComponent] = useState('track');

    const handleClick = (event) => {
        const component = event.target.innerText.toLowerCase();
        setActiveComponent(component);
        console.log(component)
    };

    const navigate = useNavigate()
    const authContext = useAuth()
    const isAuthenticated = authContext.isAuthenticated



    return (
        <Container>
        <div style={{marginTop:'20px'}}>
        <nav>
            <ul className="clickable">
                <li className={ activeComponent === 'track' ? 'active' : ''} onClick={handleClick}>Track</li>
                <li className={ activeComponent === 'get a quote' ? 'active' : ''} onClick={handleClick}>Get a Quote</li>
                {isAuthenticated && <li onClick={() => navigate(`/ship`)}>Ship</li>}
            </ul>
        </nav>
        {activeComponent === 'track' && <TrackNumberComponent />}
        {activeComponent === 'get a quote' && <QuoteComponent />}
        </div>
        </Container>
    );
}

export default WelcomeComponent;