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

    fetch: async (url, options = {}) => {
        const token = Auth.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(options.headers || {})
        };
        const response = await fetch(url, { ...options, headers });
        if (response.status === 401 || response.status === 403) {
            Auth.logout();
        }
        return response;
    }
};