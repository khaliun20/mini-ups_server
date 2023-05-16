import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../security/AuthContext';
import {
    Navbar,
    NavbarBrand,
    NavbarToggler,
    Collapse,
    Nav,
    NavItem,
    NavLink,
    Button,
} from 'reactstrap';
import { faTruck } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

function HeaderComponent() {
    const authContext = useAuth();
    const isAuthenticated = authContext.isAuthenticated;
    const [isOpen, setIsOpen] = React.useState(false);

    function toggle() {
        setIsOpen(!isOpen);
    }

    function logout() {
        authContext.logout();
    }

    return (
        <Navbar color="light" light expand="md">
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between' }}>
            <NavbarToggler/>
                <NavbarBrand tag={Link} to="/" style={{marginRight :'auto', fontFamily: 'Karla', fontSize: '50px', marginLeft: '10px' }}>
                    <FontAwesomeIcon icon={faTruck} /> Mini-UPS
                </NavbarBrand>
            <NavbarToggler onClick={toggle} />
            <Collapse isOpen={isOpen} navbar>
            <Nav className="ml-auto" navbar>
                {isAuthenticated && (
                <NavItem>
                    <NavLink tag={Link} to={`/home/${authContext.upsUser}`}>
                    Home
                    </NavLink>
                </NavItem>
                )}
                {isAuthenticated && (
                <NavItem>
                    <NavLink tag={Link} to={`/${authContext.upsUser}/packages`}>
                    See Your Packages
                    </NavLink>
                </NavItem>
                )}
                {isAuthenticated && (
                <NavItem>
                    <NavLink tag={Link} to={`/${authContext.upsUser}/labels`}>
                    See Your Orders
                    </NavLink>
                </NavItem>
                )}
                {!isAuthenticated && (
                <NavItem>
                    <NavLink tag={Link} to="/login">
                    Login
                    </NavLink>
                </NavItem>
                )}
                {isAuthenticated && (
                <NavItem>
                    <Button className="nav-link" color="link" onClick={logout}>
                    Logout
                    </Button>
                </NavItem>
                )}
            </Nav>
            </Collapse>
        </div>
        </Navbar>
    );
    }

export default HeaderComponent;