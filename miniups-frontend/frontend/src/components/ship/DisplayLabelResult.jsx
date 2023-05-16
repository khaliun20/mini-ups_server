
import React from 'react';


function DisplayLabelResultComponent({ labelResult }){
    console.log(labelResult)
    return (
        <div style={{ 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f8f9fa',
        padding: '30px',
        borderRadius: '10px'
            }}>
            <h1 style={{ marginBottom: '20px' }}>Shipping Details</h1>
            <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                backgroundColor: '#fff',
                padding: '20px',
                borderRadius: '10px',
                boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                width: '300px',
                height: '200px'
                }}>

            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{fontWeight: 'bold'}}>Username: </span>
                <span>{labelResult.username}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{fontWeight: 'bold'}}>From: </span>
                <span>({labelResult.fromx}, {labelResult.fromy})</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{fontWeight: 'bold'}}>To: </span>
                <span>({labelResult.tox}, {labelResult.toy})</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{fontWeight: 'bold'}}>Weight: </span>
                <span>{labelResult.weight} lbs</span>
            </div>
            </div>
        </div>
        
    )
}

export default DisplayLabelResultComponent