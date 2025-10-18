// Authentication utility functions

export const authService = {
  // Check if user is authenticated
  isAuthenticated: () => {
    return localStorage.getItem('isAuthenticated') === 'true';
  },

  // Get current user
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Login user
  login: (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('isAuthenticated', 'true');
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
  },

  // Get user's full name
  getUserFullName: () => {
    const user = authService.getCurrentUser();
    return user ? (user.fullName || user.username) : null;
  },

  // Get username
  getUsername: () => {
    const user = authService.getCurrentUser();
    return user ? user.username : null;
  },

  // Get user email
  getUserEmail: () => {
    const user = authService.getCurrentUser();
    return user ? user.email : null;
  }
};

export default authService;
