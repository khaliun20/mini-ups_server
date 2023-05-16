import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button } from 'reactstrap';

function AddNewPackage(props) {
    const [trackingNum, setTrackingNum] = useState('');

    function handleTrackingNumChange(event) {
        setTrackingNum(event.target.value);
    }

    function handleSubmit(event) {
        event.preventDefault();
        props.onAddNewPackage(event, trackingNum);
    }

    return (
        <Form onSubmit={handleSubmit} style={{ overflow: "scroll", marginBottom: '100px' }}>
            <FormGroup>
                <Label for="trackingNum"  style={{ fontFamily: "Karla", fontSize: "30px" }}>Tracking Number:</Label>
                <Input type="text" id="trackingNum" value={trackingNum} onChange={handleTrackingNumChange} style={{ width: '60%', margin: '0 auto', textAlign: 'center' }} />
            </FormGroup>
            <div>
                <Button type="submit"  style={{ backgroundColor: '#E86A33'}} >Add Package</Button>
                <Button type="button" onClick={props.onCancel}>Cancel</Button>
            </div>
        </Form>
    );
}




export default AddNewPackage;