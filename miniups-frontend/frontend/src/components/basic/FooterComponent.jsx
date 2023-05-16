import React from 'react';

function FooterComponent(){
    const footerStyle = {
        position: 'fixed',
        bottom: 0,
        width: '100%',
        height: '50px',
        backgroundColor: 'lightgray',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    };
    return (
        <footer className="footer" style={footerStyle} >
            ECE568 final project Mini-UPS | Haliunaa Munkhuu | Mingzhe Zhang | Xiwen Shen 
            <hr/>
        </footer>
    )
}

export default FooterComponent