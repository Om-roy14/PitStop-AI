// Automatically detect whether we are running locally or live on production
const API_BASE_URL = ['localhost', '127.0.0.1'].includes(window.location.hostname)
    ? 'http://localhost:8000'
    : 'https://pitstop-ai-production.up.railway.app'; // <--- PASTE YOUR RAILWAY URL HERE

const Auth = {
    setToken: (token) => localStorage.setItem('pitstop_token', token),
    getToken: () => localStorage.getItem('pitstop_token'),
    setUser: (user) => localStorage.setItem('user', JSON.stringify(user)),
    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    logout: () => {
        localStorage.removeItem('pitstop_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    },
    
    isAuthenticated: () => !!localStorage.getItem('pitstop_token'),
    
    protectPage: () => {
        if (!Auth.isAuthenticated()) {
            Auth.logout();
        }
    },

    // Centralized fetch wrapper
    fetch: async (url, options = {}) => {
        const token = Auth.getToken();
        
        // Base headers
        const headers = {
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(options.headers || {})
        };

        // Automatically add Content-Type if body is not FormData
        if (options.body && !(options.body instanceof FormData) && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }

        // Prepend API_BASE_URL for relative paths
        const fullUrl = url.startsWith('/') ? `${API_BASE_URL}${url}` : url;

        try {
            const response = await fetch(fullUrl, { ...options, headers });

            if (response.status === 401 || response.status === 403) {
                Auth.logout();
                return Promise.reject(new Error('Unauthorized or session expired'));
            }

            return response;
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    }
};