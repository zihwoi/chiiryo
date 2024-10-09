// src/ProtectedRoute.js
import React, { useContext } from 'react';
import { Route, Navigate } from 'react-router-dom';
import { AuthContext } from './AuthContext'; // Import your AuthContext

const ProtectedRoute = ({ element, ...rest }) => {
    const { isAuthenticated } = useContext(AuthContext); // Get authentication status from context

    return (
        <Route
            {...rest} // Spread additional props onto the Route
            element={isAuthenticated ? element : <Navigate to="/login" />} // Conditional rendering based on authentication
        />
    );
};

export default ProtectedRoute;
