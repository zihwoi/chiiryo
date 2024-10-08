// src/Projects.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './/style.css'; // Import CSS here for global styles

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
        axios.get('http://127.0.0.1:5000/api/projects')
            .then(response => {
                setProjects(response.data);
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (editingProjectId) {
            // Update existing project
            axios.put(`http://127.0.0.1:5000/api/projects/${editingProjectId}`, {
                title: title,
                description: description
            })
            .then(response => {
                console.log('Updated project data:', response.data); // Log updated project
    
                // Since response.data is the updated project, set it directly
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
            axios.post('http://127.0.0.1:5000/api/projects', { 
                title: title, 
                description: description 
            })
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
        axios.delete(`http://127.0.0.1:5000/api/projects/${id}`) // Update with your actual API endpoint
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
