// --- MOCK DATABASE ---
let complaints = [
    { id: 1, ticketId: 'HSTL-8426', room: '201A', category: 'Electrical', description: 'Fan not working.', status: 'Pending', assignedTo: null, filedOn: new Date('2024-07-20T09:00:00Z'), studentId: 'student1' },
    { id: 2, ticketId: 'HSTL-9173', room: '305B', category: 'Plumbing', description: 'Shower head is leaking constantly.', status: 'In Progress', assignedTo: 'staff1', filedOn: new Date('2024-07-19T14:30:00Z'), studentId: 'student2' },
    { id: 3, ticketId: 'HSTL-3345', room: '110A', category: 'Internet', description: 'WiFi is very slow and disconnects frequently.', status: 'Resolved', assignedTo: 'staff2', filedOn: new Date('2024-07-18T11:00:00Z'), resolvedOn: new Date('2024-07-19T16:45:00Z'), studentId: 'student1' },
    { id: 4, ticketId: 'HSTL-5821', room: '412C', category: 'Carpentry', description: 'Wardrobe door hinge is broken.', status: 'Pending', assignedTo: null, filedOn: new Date('2024-07-21T08:15:00Z'), studentId: 'student3' }
];

let announcements = [
    { id: 1, message: 'Water supply will be interrupted tomorrow from 10 AM to 12 PM for maintenance.', postedOn: new Date() },
    { id: 2, message: 'The annual hostel sports day will be held next Saturday. Please register your names with the sports secretary.', postedOn: new Date(new Date().setDate(new Date().getDate() - 2)) }
];

const maintenanceStaff = [
    { id: 'staff1', name: 'Ramesh Kumar (Plumbing)' },
    { id: 'staff2', name: 'Suresh Singh (Electrical/Internet)' },
    { id: 'staff3', name: 'Anil Verma (Carpentry)' }
];

let currentUser = null;
const MOCK_STUDENT_ID = 'student1'; // For demo purposes, we'll assume this student is logged in

// --- DOM Elements ---
const loginPage = document.getElementById('login-page');
const dashboardArea = document.getElementById('dashboard-area');
const dashboardTitle = document.getElementById('dashboard-title');

const studentDashboard = document.getElementById('student-dashboard');
const wardenDashboard = document.getElementById('warden-dashboard');
const maintenanceDashboard = document.getElementById('maintenance-dashboard');

const studentAnnouncementsContainer = document.getElementById('student-announcements');
const studentComplaintsContainer = document.getElementById('student-complaints');
const wardenComplaintsTable = document.getElementById('warden-complaints-table');
const maintenanceTasksContainer = document.getElementById('maintenance-tasks');

const complaintModal = document.getElementById('complaint-modal');
const complaintForm = document.getElementById('complaint-form');
const announcementModal = document.getElementById('announcement-modal');
const announcementForm = document.getElementById('announcement-form');

// --- AUTHENTICATION & ROUTING ---
function login(role) {
    currentUser = role;
    loginPage.classList.add('hidden');
    dashboardArea.classList.remove('hidden');
    
    switch(role) {
        case 'student':
            showStudentDashboard();
            break;
        case 'warden':
            showWardenDashboard();
            break;
        case 'maintenance':
            // In a real app, you'd have a specific staff ID. Here we'll use a mock one.
            currentUser = { role: 'maintenance', id: 'staff1' }; 
            showMaintenanceDashboard();
            break;
    }
}

function logout() {
    currentUser = null;
    loginPage.classList.remove('hidden');
    dashboardArea.classList.add('hidden');
    studentDashboard.classList.add('hidden');
    wardenDashboard.classList.add('hidden');
    maintenanceDashboard.classList.add('hidden');
}

// --- DASHBOARD RENDERING ---
function showStudentDashboard() {
    dashboardTitle.textContent = 'Student Dashboard';
    studentDashboard.classList.remove('hidden');
    renderStudentAnnouncements();
    renderStudentComplaints();
}

function showWardenDashboard() {
    dashboardTitle.textContent = 'Warden Dashboard';
    wardenDashboard.classList.remove('hidden');
    renderWardenComplaints();
}

function showMaintenanceDashboard() {
    dashboardTitle.textContent = `Maintenance Dashboard (${getStaffName(currentUser.id)})`;
    maintenanceDashboard.classList.remove('hidden');
    renderMaintenanceTasks();
}

// --- STUDENT VIEW LOGIC ---
function renderStudentAnnouncements() {
    studentAnnouncementsContainer.innerHTML = announcements
        .sort((a, b) => b.postedOn - a.postedOn)
        .map(ann => `
            <div class="border-l-4 border-indigo-500 pl-4 py-2">
                <p class="text-slate-800">${ann.message}</p>
                <p class="text-xs text-slate-500 mt-1">${ann.postedOn.toLocaleString()}</p>
            </div>
        `).join('');
    if(announcements.length === 0) {
         studentAnnouncementsContainer.innerHTML = '<p class="text-slate-500">No announcements at the moment.</p>';
    }
}

function renderStudentComplaints() {
    const myComplaints = complaints.filter(c => c.studentId === MOCK_STUDENT_ID);
    studentComplaintsContainer.innerHTML = myComplaints
        .sort((a, b) => b.filedOn - a.filedOn)
        .map(c => `
        <div class="bg-white p-6 rounded-xl shadow dashboard-card">
            <div class="flex justify-between items-start">
                <div>
                    <p class="text-sm font-semibold text-indigo-600">${c.category}</p>
                    <p class="text-xs text-slate-500">Ticket ID: ${c.ticketId}</p>
                </div>
                ${createStatusPill(c.status)}
            </div>
            <div class="mt-4">
                <p class="font-semibold text-slate-800">Room: ${c.room}</p>
                <p class="text-slate-600 mt-1">${c.description}</p>
            </div>
            <div class="mt-4 border-t pt-3 text-xs text-slate-500">
                <p>Filed on: ${c.filedOn.toLocaleString()}</p>
                ${c.assignedTo ? `<p>Assigned to: ${getStaffName(c.assignedTo)}</p>` : ''}
                ${c.resolvedOn ? `<p>Resolved on: ${c.resolvedOn.toLocaleString()}</p>` : ''}
            </div>
        </div>
    `).join('');
    if(myComplaints.length === 0) {
         studentComplaintsContainer.innerHTML = '<p class="text-slate-500 text-center col-span-full">You have not filed any complaints yet.</p>';
    }
}

// --- WARDEN VIEW LOGIC ---
function renderWardenComplaints() {
     wardenComplaintsTable.innerHTML = complaints
        .sort((a, b) => b.filedOn - a.filedOn)
        .map(c => `
        <tr class="hover:bg-slate-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">${c.ticketId}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${c.room}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${c.category}</td>
            <td class="px-6 py-4 whitespace-normal text-sm text-slate-500 max-w-xs truncate">${c.description}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${createStatusPill(c.status)}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                ${c.assignedTo ? getStaffName(c.assignedTo) : 'Not Assigned'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                ${c.status === 'Pending' ? createAssignDropdown(c.id) : ''}
            </td>
        </tr>
    `).join('');
}

// --- MAINTENANCE VIEW LOGIC ---
function renderMaintenanceTasks() {
    const myTasks = complaints.filter(c => c.assignedTo === currentUser.id && c.status !== 'Resolved');
    maintenanceTasksContainer.innerHTML = myTasks
        .sort((a, b) => a.status === 'Pending' ? -1 : 1) // Show pending first
        .map(c => `
        <div class="bg-white p-6 rounded-xl shadow dashboard-card">
             <div class="flex justify-between items-start">
                <div>
                    <p class="text-sm font-semibold text-emerald-600">${c.category}</p>
                    <p class="text-xs text-slate-500">Ticket ID: ${c.ticketId}</p>
                </div>
                ${createStatusPill(c.status)}
            </div>
            <div class="mt-4">
                <p class="font-semibold text-slate-800">Room: ${c.room}</p>
                <p class="text-slate-600 mt-1">${c.description}</p>
            </div>
            <div class="mt-4 border-t pt-3 space-x-2 flex justify-end">
                ${c.status === 'Pending' ? `<button onclick="updateStatus(${c.id}, 'In Progress')" class="px-3 py-1 text-xs font-medium text-white bg-blue-600 rounded-full hover:bg-blue-700">Start Work</button>` : ''}
                ${c.status === 'In Progress' ? `<button onclick="updateStatus(${c.id}, 'Resolved')" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded-full hover:bg-green-700">Mark as Resolved</button>`: ''}
            </div>
        </div>
    `).join('');

     if(myTasks.length === 0) {
         maintenanceTasksContainer.innerHTML = '<p class="text-slate-500 text-center col-span-full">You have no pending tasks assigned.</p>';
    }
}

// --- HELPER & UTILITY FUNCTIONS ---
function createStatusPill(status) {
    const statusClasses = {
        'Pending': 'status-pending',
        'In Progress': 'status-in-progress',
        'Resolved': 'status-resolved'
    };
    return `<span class="status-pill ${statusClasses[status]}">${status}</span>`;
}

function getStaffName(staffId) {
    const staff = maintenanceStaff.find(s => s.id === staffId);
    return staff ? staff.name : 'Unknown';
}

function createAssignDropdown(complaintId) {
    const options = maintenanceStaff.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    return `
        <select onchange="assignTask(${complaintId}, this.value)" class="text-xs rounded-md border-slate-300 focus:ring-sky-500 focus:border-sky-500">
            <option value="">Assign to...</option>
            ${options}
        </select>
    `;
}

// --- ACTIONS ---
function assignTask(complaintId, staffId) {
    if (!staffId) return;
    const complaint = complaints.find(c => c.id === complaintId);
    if (complaint) {
        complaint.assignedTo = staffId;
        complaint.status = 'In Progress';
        renderWardenComplaints();
    }
}

function updateStatus(complaintId, newStatus) {
    const complaint = complaints.find(c => c.id === complaintId);
    if (complaint) {
        complaint.status = newStatus;
        if(newStatus === 'Resolved') {
            complaint.resolvedOn = new Date();
        }
        renderMaintenanceTasks();
    }
}

// --- MODAL HANDLING ---
function openComplaintModal() { complaintModal.classList.remove('hidden'); }
function closeComplaintModal() { complaintModal.classList.add('hidden'); complaintForm.reset(); }

function openAnnouncementModal() { announcementModal.classList.remove('hidden'); }
function closeAnnouncementModal() { announcementModal.classList.add('hidden'); announcementForm.reset(); }

complaintForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const newComplaint = {
        id: complaints.length + 1,
        ticketId: `HSTL-${Math.floor(1000 + Math.random() * 9000)}`,
        room: document.getElementById('room-number').value,
        category: document.getElementById('category').value,
        description: document.getElementById('description').value,
        status: 'Pending',
        assignedTo: null,
        filedOn: new Date(),
        studentId: MOCK_STUDENT_ID
    };
    complaints.push(newComplaint);
    renderStudentComplaints();
    closeComplaintModal();
});

announcementForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const newAnnouncement = {
        id: announcements.length + 1,
        message: document.getElementById('announcement-text').value,
        postedOn: new Date()
    };
    announcements.push(newAnnouncement);
    // In a real app this would trigger a push notification or live update.
    // For now, students will see it when they next load their dashboard.
    closeAnnouncementModal();
});

// Initial check to see if a user is "logged in" from a previous session (for dev)
// In a real app, this would be handled by checking localStorage for a token
// For now, we start at the login page every time.
