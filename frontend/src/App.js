// src/App.js
import React from 'react';
import './style.css'; // Import CSS here for global styles
import { Routes, Route } from 'react-router-dom';
import NavBar from './NavBar';
import Home from './Home';
import About from './About'; // Don't forget to import About component
import Contact from './Contact'; // Don't forget to import Contact component
import Projects from './Projects';
import Login from './Login';  // Import Login component
import Register from './Register';  // Import Register component

const App = () => {
    return (
        <div>
            <NavBar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/api/projects" element={<Projects />} />
                <Route path="/contact" element={<Contact />} /> {/* Contact route correctly wrapped */}
                <Route path="/login" element={<Login />} /> {/* Add Login route */}
                <Route path="/register" element={<Register />} /> {/* Add Register route */}
            </Routes>
        </div>
    );
};

export default App;