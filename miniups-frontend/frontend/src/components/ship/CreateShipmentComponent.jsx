import axios from 'axios';
import React, { useState } from 'react';
import { useAuth } from "../security/AuthContext"
import DisplayLabelResultComponent from './DisplayLabelResult';
import {
    Row,
    Col,
    Form,
    FormGroup,
    Label,
    Input,
    Button,
    FormFeedback,
} from 'reactstrap';


function CreateShipmentComponent(){
    const [fromAddressX, setFromAddressX] = useState(0);
    const [fromAddressY, setFromAddressY] = useState(0);
    const [toAddressX, setToAddressX] = useState(0);
    const [toAddressY, setToAddressY] = useState(0);
    const [packageWeight, setPackageWeight] = useState(0);

    const [invalidInputs, setInvalidInputs] = useState([]);

    const [resFromServer, setResFromServer] = useState(null);

    const authContext = useAuth()
    const username = authContext.upsUser

    function handleInputChange(inputValue, setInput) {
        setInput(inputValue);
        // Check if input is a number and not empty
        if (isNaN(inputValue) || inputValue === '') {
        setInvalidInputs([inputValue]);
        } else {
        setInvalidInputs([]);
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        axios.post('http://vcm-30715.vm.duke.edu:8080/labels', {
            tox:  parseInt(toAddressX),
            toy: parseInt(toAddressY),
            fromx: parseInt(fromAddressX),
            fromy: parseInt(fromAddressY),
            weight: parseFloat(packageWeight) ,
            username: username
        })
        .then(response => {
            console.log(response);
            setResFromServer(response.data)
          // Handle success here
        })
        .catch(error => {
            console.log(error);
          // Handle error here
        })
    }

    return (
        <div style={{ overflow: 'scroll', marginBottom: '100px', display: 'flex', justifyContent: 'center' }}>
            
        { resFromServer === null &&          
             <Form onSubmit={handleSubmit} >
                <Row>
                <h1>Create Your Shipping Label</h1>
            <br />
                </Row>
             <Row>
                 <Col>
                 <FormGroup>
             <Label for="fromAddressX">From Address X:</Label>
             <Input
                 type="text"
                 value={fromAddressX}
                 onChange={(event) =>
                     handleInputChange(event.target.value, setFromAddressX)
                 }
                 invalid={invalidInputs.includes(fromAddressX)}
                 id="fromAddressX"
             />
             <FormFeedback>Please enter a valid number</FormFeedback>
           </FormGroup>
                 </Col>
                 <Col>
                 <FormGroup>
             <Label for="fromAddressY">From Address Y:</Label>
             <Input
               type="text"
               value={fromAddressY}
               onChange={(event) =>
                 handleInputChange(event.target.value, setFromAddressY)
               }
               invalid={invalidInputs.includes(fromAddressY)}
               id="fromAddressY"
             />
             <FormFeedback>Please enter a valid number</FormFeedback>
           </FormGroup>
                 </Col>
             </Row>
            
             <Row>
                 <Col>
                 <FormGroup>
             <Label for="toAddressX">To Address X:</Label>
             <Input
               type="text"
               value={toAddressX}
               onChange={(event) =>
                 handleInputChange(event.target.value, setToAddressX)
               }
               invalid={invalidInputs.includes(toAddressX)}
               id="toAddressX"
             />
             <FormFeedback>Please enter a valid number</FormFeedback>
           </FormGroup>
                 </Col>
                 <Col>
             
             <FormGroup>
             <Label for="toAddressX">To Address Y:</Label>
             <Input
               type="text"
               value={toAddressY}
               onChange={(event) =>
                 handleInputChange(event.target.value, setToAddressY)
               }
               invalid={invalidInputs.includes(toAddressY)}
               id="toAddresY"
             />
             <FormFeedback>Please enter a valid number</FormFeedback>
           </FormGroup>
                 </Col>
             </Row>
 
           <FormGroup>
             <Label for="packageWeight">Package Weight:</Label>
             <Input
               type="text"
               value={packageWeight}
               onChange={(event) =>
                 handleInputChange(event.target.value, setPackageWeight)
               }
               invalid={invalidInputs.includes(packageWeight)}
               id="packageWeight"
             />
             <FormFeedback>Please enter a valid number</FormFeedback>
           </FormGroup>
 
        
           <Button type="submit">Create Shipment</Button>
           </Form>
        }
        {resFromServer && <DisplayLabelResultComponent labelResult={resFromServer} />}
        </div>
    )

    
}

export default CreateShipmentComponent