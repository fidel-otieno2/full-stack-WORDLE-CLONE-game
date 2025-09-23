/**
 * Authentication service for Wordle frontend
 * Handles JWT token management and user sessions
 */

class AuthService {
  constructor() {
    this.tokenKey = 'wordle_token';
    this.usernameKey = 'wordle_username';
  }

  /**
   * Store authentication token and username
   */
  setAuthData(token, username) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.usernameKey, username);
  }

  /**
   * Get stored authentication token
   */
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Get stored username
   */
  getUsername() {
    return localStorage.getItem(this.usernameKey);
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const token = this.getToken();
    if (!token) return false;

    try {
      // Basic JWT expiration check
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  /**
   * Clear all authentication data
   */
  logout() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.usernameKey);
  }

  /**
   * Get authorization headers for API requests
   */
  getAuthHeaders() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  /**
   * Refresh token (if backend supports it)
   */
  async refreshToken() {
    // This would be implemented when backend supports token refresh
    // For now, just check if current token is still valid
    return this.isAuthenticated();
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService;
