// js/api.js
// ============================================
// Cliente API para comunicación con el backend
// ============================================

const API_URL = 'https://activities-managment.onrender.com/api';

// ============================================
// UTILIDADES
// ============================================

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function getHeaders(includeAuth = true) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (includeAuth) {
        const token = getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    
    return headers;
}

async function handleResponse(response) {
    const data = await response.json();
    
    
    return data;
}

// ============================================
// AUTH
// ============================================

const auth = {
    async login(email, password) {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: getHeaders(false),
            body: JSON.stringify({ email, password }),
        });
        
        const data = await handleResponse(response);
        setToken(data.access_token);
        return data;
    },
    
    async register(username, email, password) {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: getHeaders(false),
            body: JSON.stringify({ username, email, password }),
        });
        
        return handleResponse(response);
    },
    
    async getMe() {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    logout() {
        removeToken();
        window.location.href = '/pages/login.html';
    },
    
    isAuthenticated() {
        return !!getToken();
    }
};

// ============================================
// ACTIVITIES
// ============================================

const activities = {
    async getAll(filters = {}) {
        const params = new URLSearchParams();
        
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== '') {
                params.append(key, value);
            }
        });
        
        const response = await fetch(`${API_URL}/activities?${params}`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async getById(id) {
        const response = await fetch(`${API_URL}/activities/${id}`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async create(data) {
        const response = await fetch(`${API_URL}/activities`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async update(id, data) {
        const response = await fetch(`${API_URL}/activities/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async changeState(id, state) {
        const response = await fetch(`${API_URL}/activities/${id}/state`, {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ state }),
        });
        
        return handleResponse(response);
    },
    
    async delete(id) {
        const response = await fetch(`${API_URL}/activities/${id}`, {
            method: 'DELETE',
            headers: getHeaders(),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Error al eliminar');
        }
        
        return true;
    }
};

// ============================================
// CATEGORIES
// ============================================

const categories = {
    async getAll() {
        const response = await fetch(`${API_URL}/categories`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async getById(id) {
        const response = await fetch(`${API_URL}/categories/${id}`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async create(data) {
        const response = await fetch(`${API_URL}/categories`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async update(id, data) {
        const response = await fetch(`${API_URL}/categories/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async delete(id) {
        const response = await fetch(`${API_URL}/categories/${id}`, {
            method: 'DELETE',
            headers: getHeaders(),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Error al eliminar');
        }
        
        return true;
    }
};

// ============================================
// USERS
// ============================================

const users = {
    async getAll(filters = {}) {
        const params = new URLSearchParams(filters);
        
        const response = await fetch(`${API_URL}/users?${params}`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async getById(id) {
        const response = await fetch(`${API_URL}/users/${id}`, {
            headers: getHeaders(),
        });
        
        return handleResponse(response);
    },
    
    async create(data) {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async update(id, data) {
        const response = await fetch(`${API_URL}/users/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        
        return handleResponse(response);
    },
    
    async delete(id) {
        const response = await fetch(`${API_URL}/users/${id}`, {
            method: 'DELETE',
            headers: getHeaders(),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Error al eliminar');
        }
        
        return true;
    }
};

// ============================================
// EXPORTAR
// ============================================

export { auth, activities, categories, users, getToken, removeToken };