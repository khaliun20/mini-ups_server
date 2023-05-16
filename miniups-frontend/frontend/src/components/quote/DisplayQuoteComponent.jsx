import React, { useState } from 'react';
import AvailableQuotesComponent from './AvailabeQuotesComponent';
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

function DisplayQuoteComponent() {
    const [fromAddressX, setFromAddressX] = useState('');
    const [fromAddressY, setFromAddressY] = useState('');
    const [toAddressX, setToAddressX] = useState('');
    const [toAddressY, setToAddressY] = useState('');
    const [packageWeight, setPackageWeight] = useState('');
    const [packageLength, setPackageLength] = useState('');
    const [packageWidth, setPackageWidth] = useState('');
    const [packageHeight, setPackageHeight] = useState('');
    const [quote, setQuote] = useState(null);
    const [invalidInputs, setInvalidInputs] = useState([]);

    function handleSubmit(event) {
        event.preventDefault();
        const inputs = [
            fromAddressX,
            fromAddressY,
            toAddressX,
            toAddressY,
            packageWeight,
            packageLength,
            packageWidth,
            packageHeight,
    ];

    // Check if all inputs are numbers
    if (inputs.some((input) => isNaN(input))) {
        setInvalidInputs(inputs.filter((input) => isNaN(input)));
        return;
    }

    const distance =
      Math.sqrt(fromAddressX * fromAddressX + fromAddressX * fromAddressX) -
      Math.sqrt(fromAddressY * fromAddressY + toAddressY * toAddressY);

    const price = Math.abs(distance) * packageWeight * 3;
    setQuote(price);
    }

    function handleInputChange(inputValue, setInput) {
        setInput(inputValue);
        // Check if input is a number and not empty
        if (isNaN(inputValue) || inputValue === '') {
        setInvalidInputs([inputValue]);
        } else {
        setInvalidInputs([]);
        }
    }

    return (
    <div style={{ overflow: 'scroll', marginBottom: '100px', display: 'flex', justifyContent: 'center' }}>
        {quote == null && (
        <Form onSubmit={handleSubmit} >
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

       
          <Button type="submit">Get Quote</Button>
        </Form>
      )}
      {quote && (
        <div>
          <AvailableQuotesComponent basicRate={quote} />
        </div>
      )}
    </div>
  );
}

export default DisplayQuoteComponent;
