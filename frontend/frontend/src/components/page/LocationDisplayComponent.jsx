import React from 'react';
import packageIcon from '../image/fast-delivery.png';
import img from '../image/map_background.jpg'


function LocationDisplayComponent({x, y}) {

     // Define the container style
    const containerStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
        // width: '500px',
        // height: '500px',
        width: '500px',
        height: '500px',
        border: '1px solid black',
        backgroundImage: `url(${img})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    }

    const positionX = x >= 0 ? Math.min(x, 40) : Math.max(x, -40);
    const positionY = y >= 0 ? Math.min(y, 45) : Math.max(y, -45);

    const rangeStyle = {
        position: 'absolute',
        top: `${positionY + 50}%`,
        left: `${positionX + 50}%`,
        border: '2px solid red',
        boxSizing: 'border-box',
    }
    const packageStyle = {
        width: '60px',
        height: '60px',
        position: 'absolute',
        top: `${positionY + 50}%`,
        left: `${positionX + 50}%`,
        transform: 'translate(-50%, -50%)',
    };

    const legendStyle = {
        position: 'absolute',
        top: 'calc(100% + 20px)',
        left: '50%',
        transform: 'translateX(-50%)',
        // zIndex: '1',
        fontWeight: 'bold',
        textShadow: '1px 1px 1px black',
        whiteSpace: 'nowrap',
    };


    return (
        <div style={containerStyle}>
            <div style={rangeStyle}>
                <p style={legendStyle} >({x}, {y})</p>
                <img src={packageIcon} alt="Package" style={packageStyle} />
            </div>
        </div>
    )

}



export default LocationDisplayComponent;