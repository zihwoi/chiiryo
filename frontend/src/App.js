// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './Home';
import About from './About'; // Don't forget to import About component
import Contact from './Contact'; // Don't forget to import Contact component
import Projects from './Projects';

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/projects" element={<Projects />} />
                    {/* Add other routes here */}
                </Routes>
            </div>
        </Router>
    );
};

export default App;
