// static/js/dashboard.js

async function loadDashboardStats() {
    const stats = await fetchDashboardStats();

    if (stats) {
        document.getElementById('totalProjects').textContent = stats.total_projects || 0;
        document.getElementById('totalSanctioned').textContent = '₹' + (stats.total_sanctioned || 0) + ' Cr';
        document.getElementById('totalSpent').textContent = '₹' + (stats.total_spent || 0) + ' Cr';
        document.getElementById('flaggedCount').textContent = stats.flagged_count || 0;
    } else {
        document.getElementById('totalProjects').textContent = 'N/A';
        document.getElementById('totalSanctioned').textContent = 'N/A';
        document.getElementById('totalSpent').textContent = 'N/A';
        document.getElementById('flaggedCount').textContent = 'N/A';
    }
}

async function loadFlaggedProjectsTable() {
    const projects = await fetchFlaggedProjects();
    const tableBody = document.getElementById('flaggedTable');

    if (!tableBody) return;

    if (projects && projects.length > 0) {
        let html = '';
        projects.slice(0, 5).forEach(project => {
            const amount = project.sanction_amount
                ? '₹' + (project.sanction_amount / 100000).toFixed(1) + 'L'
                : 'N/A';
            html += `
                <tr>
                    <td>${project.work_name || 'Unknown'}</td>
                    <td>${amount}</td>
                    <td><span class="badge bg-danger">Flagged</span></td>
                </tr>
            `;
        });
        tableBody.innerHTML = html;
    } else {
        tableBody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No flagged projects found</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    loadDashboardStats();
    loadFlaggedProjectsTable();
});