// Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Change useHistory to useNavigate

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorData, setErrorData] = useState(null); // Add state for error messages
    const navigate = useNavigate(); // Use useNavigate instead of useHistory

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            // Registration successful, redirect to login or another page
            navigate('/login'); // Use navigate instead of history.push
        } else {
            const errorData = await response.json(); // Get error data from response
            console.error('Registration failed:', errorData.message); // Log the error message

            // Show the error message to the user
            setErrorData(`Registration failed: ${errorData.message}`); // Set error message in state
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Register</h1>
            {errorData && <p style={{ color: 'red' }}>{errorData}</p>} {/* Display error message */}
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
