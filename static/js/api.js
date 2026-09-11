// static/js/api.js

// Base URL for API calls
const API_BASE = '';

// Fetch all projects
async function fetchProjects() {
    try {
        const response = await fetch(`${API_BASE}/api/projects`);
        if (!response.ok) throw new Error('Failed to fetch projects');
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        return [];
    }
}

// Fetch flagged projects
async function fetchFlaggedProjects() {
    try {
        const response = await fetch(`${API_BASE}/api/flagged`);
        if (!response.ok) throw new Error('Failed to fetch flagged projects');
        return await response.json();
    } catch (error) {
        console.error('Error fetching flagged projects:', error);
        return [];
    }
}

// Fetch project details by ID
async function fetchProjectDetails(projectId) {
    try {
        const response = await fetch(`${API_BASE}/api/projects/${projectId}`);
        if (!response.ok) throw new Error('Failed to fetch project details');
        return await response.json();
    } catch (error) {
        console.error('Error fetching project details:', error);
        return null;
    }
}

// Fetch dashboard statistics
async function fetchDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard/stats`);
        if (!response.ok) throw new Error('Failed to fetch dashboard stats');
        return await response.json();
    } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        return null;
    }
}

// Export flagged projects (PDF)
async function exportFlaggedReport() {
    window.location.href = `${API_BASE}/api/export/flagged`;
}