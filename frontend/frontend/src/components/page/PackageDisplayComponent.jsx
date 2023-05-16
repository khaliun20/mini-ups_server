import React from 'react';
import { useNavigate } from "react-router-dom";
import { Table, Button } from 'reactstrap';
import { Fragment } from 'react';

function PackageDisplayComponent({ packageInfo }){
    const navigate = useNavigate()

    function updateLocation(trackingNum){
        navigate(`/packages/${trackingNum}`)
    }

    function checkDetail(trackingNum){
        // console.log("click")
        navigate(`/packages/${trackingNum}/items`)
    }

    return (
        <div className="container" style={{ marginTop: '50px', marginBottom: '50px' }}>
        <Table>
            <thead>
            <tr>
                <th>ID</th>
                <th>State</th>
                <th>Tracking Number</th>
                <th>Item Detail</th>
                <th>Deliver Address x</th>
                <th>Deliver Address y</th>
                <th>Update Address</th>
            </tr>
            </thead>
            <tbody>
            {packageInfo.map((package_) => (
                <Fragment key={package_.packagesId}>
                <tr>
                    <td>{package_.packagesId}</td>
                    <td>{package_.state}</td>
                    <td>{package_.truckingNum}</td>
                    <td>
                    <Button
                        color="success"
                        onClick={() => checkDetail(package_.truckingNum)}
                        style={{ backgroundColor: '#7C9070'}} 
                    >
                        Check Detail
                    </Button>
                    </td>
                    <td>{package_.x}</td>
                    <td>{package_.y}</td>
                    <td>
                    <Button
                        color="success"
                        onClick={() => updateLocation(package_.truckingNum)}
                        disabled={
                        package_.state === 'delivering' ||
                        package_.state === 'delivered'
                        }
                        style={{ backgroundColor: '#7C9070' }} 
                    >
                        Update
                    </Button>
                    </td>
                </tr>
                </Fragment>
            ))}
            </tbody>
        </Table>
        </div>
    );
}


export default PackageDisplayComponent