// src/About.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const About = () => {
    const [funActivities, setFunActivities] = useState([]);

    // Fetch data from the API when the component is mounted
    useEffect(() => {
        const fetchFunActivities = async () => {
            try {
                const response = await axios.get('http://localhost:5000/about');
                setFunActivities(response.data.fun_activities); // Set the fetched data
            } catch (error) {
                console.error("Error fetching the fun activities:", error);
            }
        };
        fetchFunActivities();
    }, []);

    return (
        <div>
            <h1>About Chiiryo</h1>
            <p>Chiiryo is your creative project manager. Our goal is to help you manage your projects effectively and creatively.</p>
            <a href="/">Back to home</a>

            <h2>What We Love to Create</h2>
            <ul>
                {funActivities.length > 0 ? (
                    funActivities.map((activity, index) => (
                        <li key={index}>{activity}</li>
                    ))
                ) : (
                    <li>Loading activities...</li> // Display a message if no data is loaded
                )}
            </ul>
        </div>
    );
}

export default About;
