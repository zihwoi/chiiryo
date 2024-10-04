// src/App.js
import React from 'react';
import MyComponent from './MyComponent'; // Import your custom component

function App() {
  return (
    <div>
      <h1>Welcome to My React App!</h1> {/* Change the title */}
      <p>This is a simple React application to demonstrate changes.</p>
      <MyComponent /> {/* Use your custom component */}
    </div>
  );
}

export default App;
