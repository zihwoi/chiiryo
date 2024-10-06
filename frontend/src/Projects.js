// src/Projects.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './/style.css'; // Import CSS here for global styles

const Projects = () => {
    const [projects, setProjects] = useState([]);
    const [projectTitle, setProjectTitle] = useState('');
    const [projectDescription, setProjectDescription] = useState('');
    

    useEffect(() => {
        // Fetch projects from your Flask backend
        axios.get('http://127.0.0.1:5000/api/projects') // Update with your actual API endpoint
            .then(response => {
                setProjects(response.data);
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
            });
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/manage_projects', { title: projectTitle, description: projectDescription })
            .then(response => {
                // Refresh project list after creating a new project
                setProjects([...projects, response.data]);
                setProjectTitle('');
                setProjectDescription('');
            })
            .catch(error => {
                console.error('Error creating project:', error);
            });
    };

    const handleDelete = (id) => {
        axios.delete(`/api/delete_project/${id}`) // Update with your actual API endpoint
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
                    <label htmlFor="project_title">Project Title</label>
                    <input
                        type="text"
                        id="project_title"
                        name="project_title"
                        placeholder="Enter project title"
                        value={projectTitle}
                        onChange={(e) => setProjectTitle(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="project_description">Project Description</label>
                    <textarea
                        id="project_description"
                        name="project_description"
                        placeholder="Enter project description"
                        rows="4"
                        value={projectDescription}
                        onChange={(e) => setProjectDescription(e.target.value)}
                        required
                    />
                </div>

                <button type="submit" className="btn-submit">Create Project</button>
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
