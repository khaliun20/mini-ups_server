import React from 'react';
import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { useAuth } from "../security/AuthContext"
import { getUser } from '../api/upsAuthService'
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';

function LoginComponent(){
    const [ username, setUsername] = useState('abc')
    const [ password, setPassword] = useState('password')
    const [ errorMessage, setErrorMessage] = useState(false)

    const navigate = useNavigate()
    const authContext = useAuth()

    function handleUsernameChange(event){
        setUsername(event.target.value)
    }

    function handlePasswordChange(event){
        setPassword(event.target.value)
    }

    function handleSubmit(event) {
        getUser(username)
            .then(response => {
            const user = response.data;
            if (user && user.password === password) {
                authContext.setIsAuthenticated(true);
                authContext.setUpsUser(username);
                localStorage.setItem('user', username);
                navigate(`/home/${username}`);
            } else {
                setErrorMessage(true);
            }
        })
        .catch(error => {
            console.error(error);
            setErrorMessage(true);
        });
    }


    return (
        <div style={{ backgroundColor : 'F6F1F1'}}>
        <Container>
            { errorMessage &&  <Alert color="danger">Authentication Failed</Alert> }
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
                            <Button style={{ backgroundColor: '#C9DBB2', fontSize: '1.5rem' }} type="button" name="login" onClick={handleSubmit}>Log in</Button>
                        </FormGroup>
                        <FormGroup>
                            <Link className="nav-link" to={`/signup`} style={{ fontFamily: 'Karla', fontSize: "20px" }}>Don't have an account yet? Sign up here</Link>
                        </FormGroup>
                    </Form>
                </Col>
            </Row>
        </Container>
        </div>

    )
}

export default LoginComponent

