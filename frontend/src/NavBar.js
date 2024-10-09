import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
    return (
        <nav style={navStyle}>
            <h2 style={titleStyle}>Chiiryo</h2>
            <ul style={listStyle}>
                <li style={listItemStyle}><Link to="/">Home</Link></li>
                <li style={listItemStyle}><Link to="/about">About</Link></li>
                <li style={listItemStyle}><Link to="/api/projects">Projects</Link></li>
                <li style={listItemStyle}><Link to="/contact">Contact</Link></li>
                <li style={listItemStyle}><Link to="/login">Login</Link></li> {/* Link to Login */}
                <li style={listItemStyle}><Link to="/register">Register</Link></li> {/* Link to Register */}
            </ul>
        </nav>
    );
};

const navStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundColor: '#282c34',
    color: 'white'
};

const titleStyle = {
    margin: 0,
};

const listStyle = {
    listStyleType: 'none',
    display: 'flex',
    margin: 0,
    padding: 0,
};

const listItemStyle = {
    margin: '0 10px',
};

export default NavBar;
