// src/App.js

import React from 'react';
import './/style.css'; // Import CSS here for global styles
import { Routes, Route } from 'react-router-dom';
import NavBar from './NavBar';
import Home from './Home';
import About from './About'; // Don't forget to import About component
import Contact from './Contact'; // Don't forget to import Contact component
import Projects from './Projects';

const App = () => {
    return (
        <div>
            <NavBar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/contact" element={<Contact />} />
            </Routes>
        </div>
    );
};

export default App;