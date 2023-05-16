import React from 'react';
import { Table } from 'reactstrap';
import { Fragment } from 'react';

function AllShippingLabelComponent({ shippingLabelInfo }){
    return (
        <div className="container" style={{ marginTop: '50px', marginBottom: '50px' }}>
        <Table>
            <thead>
            <tr>
                <th>ID</th>
                <th>From Address X</th>
                <th>From Address Y</th>
                <th>To Address X</th>
                <th>To Address Y</th>
                <th>Weight</th>
            </tr>
            </thead>
            <tbody>
            {shippingLabelInfo.map((label) => (
                <Fragment key={label.id}>
                <tr>
                    <td>{label.id}</td>
                    <td>{label.fromx}</td>
                    <td>{label.fromy}</td>
                    <td>{label.tox}</td>
                    <td>{label.toy}</td>
                    <td>{label.weight}</td>
                </tr>
                </Fragment>
            ))}
            </tbody>
        </Table>
        </div>
    );
}

export default AllShippingLabelComponent