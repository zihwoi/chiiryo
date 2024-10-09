// src/Projects.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Projects = () => {
    const [projects, setProjects] = useState([]);
    const [editingProjectId, setEditingProjectId] = useState(null);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    //fetch projects from backend
    useEffect(() => {
        fetchProjects();
    }, []);

    const fetchProjects = () => {
        const token = localStorage.getItem('token'); // Get the token from local storage

        // Make sure to include the base URL if it's not defined elsewhere
        axios.get('/api/projects', { // Correctly format the URL
            headers: {
                Authorization: `Bearer ${token}`, // Include token in headers
            },
        })
            .then(response => {
                setProjects(response.data);
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const token = localStorage.getItem('token'); // Get the token from local storage

        // Check if token exists before proceeding
        if (!token) {
            console.error('No token found, unable to submit project.');
            return; // Exit the function early if no token
        }

        const headers = {
            headers: {
                Authorization: `Bearer ${token}`, // Include token in headers
            },
        };

        if (editingProjectId) {
            // Update existing project
            axios.put(`/api/projects/${editingProjectId}`, {
                title: title,
                description: description
            }, headers) // Add headers here
                .then(response => {
                    console.log('Updated project data:', response.data); // Log updated project

                    // Update the projects state with the modified project
                    setProjects(projects.map(project =>
                        project.id === editingProjectId ? response.data : project
                    ));
                    resetForm();
                })
                .catch(error => {
                    console.error('Error updating project:', error);
                });
        } else {
            // Create new project
            axios.post('/api/projects', {
                title: title,
                description: description
            }, headers) // Add headers here
                .then(response => {
                    console.log('Created project data:', response.data); // Log created project
                    setProjects([...projects, response.data]);
                    resetForm();
                })
                .catch(error => {
                    console.error('Error creating project:', error);
                });
        }
    };

    const handleEdit = (project) => {
        setTitle(project.title);
        setDescription(project.description);
        setEditingProjectId(project.id);
    };

    const resetForm = () => {
        setTitle('');
        setDescription('');
        setEditingProjectId(null);
    };

    const handleDelete = (id) => {
        const token = localStorage.getItem('token'); // Get the token from local storage

        // Check if token exists before proceeding
        if (!token) {
            console.error('No token found, unable to delete project.');
            return; // Exit the function early if no token
        }

        const headers = {
            headers: {
                Authorization: `Bearer ${token}`, // Include token in headers
            },
        };

        axios.delete(`/api/projects/${id}`, headers) // Include headers here
            .then(() => {
                // Remove the deleted project from the list
                setProjects(projects.filter(project => project.id !== id));
            })
            .catch(error => {
                console.error('Error deleting project:', error);
            });
    };


    return (
        <div>
            <h1>My Projects</h1>

            {/* Project Creation Form */}
            <form onSubmit={handleSubmit} className="project-form">
                <div className="form-group">
                    <label htmlFor="title">Project Title</label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        placeholder="Enter project title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="description">Project Description</label>
                    <textarea
                        id="description"
                        name="description"
                        placeholder="Enter project description"
                        rows="4"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </div>

                <button type="submit" className="btn-submit">
                    {editingProjectId ? 'Update Project' : 'Create Project'}
                </button>
                {editingProjectId && (
                    <button type="button" onClick={resetForm} className="btn btn-cancel">
                        Cancel Edit
                    </button>
                )}
            </form>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {projects.length > 0 ? (
                        projects.map(project => (
                            <tr key={project.id}>
                                <td>{project.id}</td>
                                <td>{project.title}</td>
                                <td>{project.description}</td>
                                <td>{project.created_at}</td>
                                <td>
                                    <div className="button-group">
                                        <button className="btn btn-edit" onClick={() => handleEdit(project)}>Edit</button>
                                        <button className="btn btn-delete" onClick={() => handleDelete(project.id)}>Delete</button>
                                    </div>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5">No projects found.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Projects;
