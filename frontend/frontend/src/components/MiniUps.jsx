import React from 'react';
import { BrowserRouter, Route, Routes, Navigate} from "react-router-dom"
import "./MiniUps.css"
import LogOutComponent from "./basic/LogoutComponent"
import FooterComponent from "./basic/FooterComponent"
import HeaderComponent from "./basic/HeaderComponent"
import UserPackageComponent from "./page/UserPackageComponent"
import LoginComponent from "./basic/LoginComponent"
import SignUpComponent from "./basic/SignUpComponent"
import WelcomeComponent from "./WelcomeComponent"
import ErrorComponent from "./basic/ErrorComponent"
import AuthProvider, { useAuth } from "./security/AuthContext"
import UpdateAddressComponent from "./page/UpdateAddressComponent"
import ItemsInfoComponent from "./page/ItemsInfoComponent"
import QuoteComponent from './quote/QuoteComponent';
import CreateShipmentComponent from './ship/CreateShipmentComponent';
import UserAllLabelComponent from './ship/UserAllLabelsComponent';



function AuthenticatedRoute({ children }){
    const authContext = useAuth()
    if(authContext.isAuthenticated)
        return children
    return <Navigate to="/" />
}


export default function MiniUps(){

    
    return (
        <div className="MiniUps">
            <AuthProvider>
                <BrowserRouter>
                <HeaderComponent />
                    <Routes>
                        <Route path="/" element={ <WelcomeComponent /> }></Route>
                        <Route path="/login" element={ <LoginComponent /> }></Route>
                        <Route path="/logout" element={ <LogOutComponent /> }></Route>
                        <Route path="/signup" element={ <SignUpComponent /> }></Route>
                        <Route path="/quote" element={ <QuoteComponent /> }></Route>
                        <Route path="/ship" element={ <CreateShipmentComponent/> }></Route>
                        <Route path="/packages/:trackingNum" element={ <UpdateAddressComponent /> }></Route>
                        <Route path="/packages/:trackingNum/items" element={ <ItemsInfoComponent /> }></Route>
                        <Route path="/home/:username" element={ 
                            <AuthenticatedRoute> 
                                <WelcomeComponent />
                            </AuthenticatedRoute>  }>
                        </Route>
                        <Route path="/:username/packages" element={ 
                            <AuthenticatedRoute> 
                                <UserPackageComponent />
                            </AuthenticatedRoute>  }>
                        </Route>
                        <Route path="/:username/labels" element={ 
                            <AuthenticatedRoute> 
                                <UserAllLabelComponent />
                            </AuthenticatedRoute>  }>
                        </Route>
                        <Route path="*" element={ 
                            <AuthenticatedRoute>
                                <ErrorComponent />
                            </AuthenticatedRoute>   }>
                        </Route>
                    </Routes>
                    <FooterComponent />
                </BrowserRouter>
            </AuthProvider>

            
        </div>
    )
}



















