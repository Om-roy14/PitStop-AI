// Automatically detect whether we are running locally or live on Vercel
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://your-actual-railway-url.up.railway.app'; // <--- PASTE YOUR RAILWAY URL HERE

const Auth = {
    setToken: (token) => localStorage.setItem('pitstop_token', token),
    getToken: () => localStorage.getItem('pitstop_token'),
    logout: () => {
        localStorage.removeItem('pitstop_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    },
    isAuthenticated: () => !!localStorage.getItem('pitstop_token'),
    
    protectPage: () => {
        if (!Auth.isAuthenticated()) {
            window.location.href = '/login';
        }
    },

    // Centralized fetch wrapper: automatically prepends the correct base URL
    fetch: async (url, options = {}) => {
        const token = Auth.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(options.headers || {})
        };

        // If the URL starts with /api or doesn't have http, prepend API_BASE_URL
        let fullUrl = url;
        if (url.startsWith('/')) {
            fullUrl = `${API_BASE_URL}${url}`;
        }

        const response = await fetch(fullUrl, { ...options, headers });
        if (response.status === 401 || response.status === 403) {
            Auth.logout();
        }
        return response;
    }
};