// js/utils.js
// ============================================
// Utilidades de UI
// ============================================

// ============================================
// NOTIFICACIONES (Toast)
// ============================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500',
    };
    
    const toast = document.createElement('div');
    toast.className = `${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg mb-2 transform transition-all duration-300 translate-x-full`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 10);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'fixed top-4 right-4 z-50';
    document.body.appendChild(container);
    return container;
}

// ============================================
// MODAL
// ============================================

function showModal(content, options = {}) {
    const { title = '', onConfirm = null, onCancel = null, confirmText = 'Confirmar', cancelText = 'Cancelar' } = options;
    
    const modal = document.createElement('div');
    modal.id = 'modal-overlay';
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    
    modal.innerHTML = `
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all">
            ${title ? `<div class="px-6 py-4 border-b"><h3 class="text-lg font-semibold text-gray-900">${title}</h3></div>` : ''}
            <div class="px-6 py-4">
                ${typeof content === 'string' ? content : ''}
            </div>
            <div class="px-6 py-4 border-t flex justify-end gap-3">
                <button id="modal-cancel" class="btn-secondary">${cancelText}</button>
                <button id="modal-confirm" class="btn-primary">${confirmText}</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Event listeners
    modal.querySelector('#modal-cancel').addEventListener('click', () => {
        closeModal();
        if (onCancel) onCancel();
    });
    
    modal.querySelector('#modal-confirm').addEventListener('click', () => {
        closeModal();
        if (onConfirm) onConfirm();
    });
    
    // Cerrar con click fuera
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
            if (onCancel) onCancel();
        }
    });
}

function closeModal() {
    const modal = document.getElementById('modal-overlay');
    if (modal) modal.remove();
}

// ============================================
// CONFIRM DIALOG
// ============================================

function confirm(message, onConfirm) {
    showModal(`<p class="text-gray-600">${message}</p>`, {
        title: 'Confirmar acción',
        onConfirm,
        confirmText: 'Sí, continuar',
        cancelText: 'Cancelar'
    });
}

// ============================================
// LOADING SPINNER
// ============================================

function showLoading(container) {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.className = 'flex items-center justify-center py-8';
    spinner.innerHTML = `
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    `;
    
    if (typeof container === 'string') {
        container = document.querySelector(container);
    }
    
    container.innerHTML = '';
    container.appendChild(spinner);
}

function hideLoading(container) {
    if (typeof container === 'string') {
        container = document.querySelector(container);
    }
    
    const spinner = container.querySelector('#loading-spinner');
    if (spinner) spinner.remove();
}

// ============================================
// FORMATTERS
// ============================================

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ============================================
// STATE/PRIORITY LABELS
// ============================================

const stateLabels = {
    pendiente: 'Pendiente',
    en_progreso: 'En Progreso',
    bloqueada: 'Bloqueada',
    completada: 'Completada',
    cancelada: 'Cancelada'
};

const priorityLabels = {
    baja: 'Baja',
    media: 'Media',
    alta: 'Alta',
    urgente: 'Urgente'
};

function getStateLabel(state) {
    return stateLabels[state] || state;
}

function getPriorityLabel(priority) {
    return priorityLabels[priority] || priority;
}

// ============================================
// EXPORTAR
// ============================================

export { 
    showToast, 
    showModal, 
    closeModal, 
    confirm, 
    showLoading, 
    hideLoading,
    formatDate,
    formatDateTime,
    getStateLabel,
    getPriorityLabel,
    stateLabels,
    priorityLabels
};