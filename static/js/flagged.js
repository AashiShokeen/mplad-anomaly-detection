// static/js/flagged.js

let allFlagged = [];

async function loadFlaggedProjects() {
    allFlagged = await fetchFlaggedProjects();
    applyFilters();
}

function applyFilters() {
    const tableBody = document.getElementById('flaggedTableBody');
    if (!tableBody) return;

    const searchQuery = document.getElementById('searchInput')?.value?.toLowerCase() || '';
    const districtFilter = document.getElementById('districtFilter')?.value || '';
    const reasonFilter = document.getElementById('reasonFilter')?.value || '';

    let filtered = allFlagged || [];

    if (searchQuery) {
        filtered = filtered.filter(p =>
            (p.work_name || '').toLowerCase().includes(searchQuery)
        );
    }
    if (districtFilter) {
        filtered = filtered.filter(p => p.district === districtFilter);
    }
    if (reasonFilter) {
        filtered = filtered.filter(p => p.anomaly_type === reasonFilter);
    }

    if (filtered.length > 0) {
        let html = '';
        filtered.forEach((project, index) => {
            const reason = project.anomaly_type || 'unknown';
            const badgeClass = reason === 'cost_outlier' ? 'danger' :
                               reason === 'stalled' ? 'warning' : 'info';
            const amount = project.sanction_amount
                ? '₹' + (project.sanction_amount / 100000).toFixed(1) + 'L'
                : 'N/A';

            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${project.work_name || 'Unknown'}</td>
                    <td>${project.district || 'N/A'}</td>
                    <td>${amount}</td>
                    <td><span class="badge bg-${badgeClass}">${reason.replace('_', ' ')}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewProject(${project.project_id || project.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        tableBody.innerHTML = html;
    } else {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No flagged projects found</td></tr>';
    }
}

function viewProject(id) {
    window.location.href = `/projects/${id}`;
}

document.addEventListener('DOMContentLoaded', function () {
    loadFlaggedProjects();

    document.getElementById('searchInput')?.addEventListener('keyup', applyFilters);
    document.getElementById('districtFilter')?.addEventListener('change', applyFilters);
    document.getElementById('reasonFilter')?.addEventListener('change', applyFilters);
});