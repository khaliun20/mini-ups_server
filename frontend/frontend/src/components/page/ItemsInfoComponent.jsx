import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { retrieveAllItemsInPackage } from '../api/trackingApiService';
import { Container, Table } from 'reactstrap';

function ItemsInfoComponent() {
    const { trackingNum } = useParams();
    const [ items, setItems ] = useState([]);


    useEffect(() => {
        retrieveAllItemsInPackage(trackingNum)
        .then((response) => {
            console.log(response.data)
            setItems(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    }, [trackingNum]);

    return (
        <Container>
        <br/>
        <h1>Items for Tracking Number: {trackingNum}</h1>
        <Table responsive style={{ marginTop: '50px', marginBottom: '100px' }}>
            <thead>
            <tr>
                <th>Description</th>
                <th>Quantity</th>
            </tr>
            </thead>
            <tbody>
            {items.map((item) => (
                <tr key={item.id}>
                <td>{item.description}</td>
                <td>{item.quantity}</td>
                </tr>
            ))}
            </tbody>
        </Table>
        </Container>
    );

    // return (
    //     <div className="container">
    //         <h1>Items for Tracking Number: {trackingNum}</h1>
    //             <div className="container">
    //             <table className="table">
    //                 <thead>
    //                     <tr>
    //                         <th>Description</th>
    //                         <th>Quantity</th>
    //                     </tr>
    //                 </thead>
    //                 <tbody>
    //                     <tr></tr>
    //                     {items.map((item) => (
    //                         <tr key={ item.id } >
    //                             <td> { item.description }</td>
    //                             <td> { item.quantity } </td>
    //                         </tr>
    //                     ))}
    //                 </tbody>
    //             </table>
    //             </div>
    //     </div>
    // );
}

export default ItemsInfoComponent;
