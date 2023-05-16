import React from 'react';
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from 'axios'
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';



function SignUpComponent(){

    const [username, setUsername] = useState()
    const [password, setPassword] = useState()
    const [erroMsg, setErrorMsg ] = useState()

    const navigate = useNavigate()

    function handleUsernameChange(event){
        setUsername(event.target.value)
    }

    function handlePasswordChange(event){
        setPassword(event.target.value)
    }

    //* change to virtual machine if need
    function handleSubmit() {
        axios.post('http://vcm-30715.vm.duke.edu:8080/api/users', {
            username: username,
            password: password,
            state : "active"
        })
        .then(function (response) {
            navigate(`/login`)
        })
        .catch(function (error) {
          // handle error
            if(error.response.status === 409){
                setErrorMsg("User Account already exist, try a new one.")
            }
            console.log(error);
        });
    }


    return (
        <div className="SignUp">
            <h1>Sign Up: </h1>
            { erroMsg &&  <Alert color="danger">{erroMsg}</Alert> }
            <Container>
            <Row className="justify-content-center">
                <Col md={6}>
                    <Form>
                        <FormGroup>
                            <Label style={{ fontFamily: 'Karla', fontSize: "30px" }} for="username">User Name:</Label>
                            <Input type="text" name="username" id="username" value={username} onChange={handleUsernameChange} placeholder="Enter your username" style={{ width: '60%', margin: '0 auto', textAlign: 'center' }}/>
                        </FormGroup>
                        <FormGroup>
                            <Label style={{ fontFamily: 'Karla', fontSize: "30px" }} for="password">Password:</Label>
                            <Input type="password" name="password" id="password" onChange={handlePasswordChange} placeholder="Enter your password" style={{ width: '60%', margin: '0 auto', textAlign: 'center' }} />
                        </FormGroup>
                        <FormGroup>
                            <Button style={{ backgroundColor: '#C9DBB2', fontSize: '1.5rem' }} type="button" name="login" onClick={handleSubmit}>Sign up</Button>
                        </FormGroup>
                    </Form>
                </Col>
            </Row>
        </Container>
        </div>
    )
}

export default SignUpComponent