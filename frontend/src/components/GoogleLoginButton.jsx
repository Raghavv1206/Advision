// frontend/src/components/GoogleLoginButton.jsx - TRY ORIGIN ONLY
import React from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import toast from 'react-hot-toast';

export default function GoogleLoginButton() {
  const navigate = useNavigate();

  // Try using just the origin (no path)
  const redirectUri = window.location.origin; // Just http://localhost:5173

  const handleLogin = async (googleResponse) => {
    const toastId = toast.loading('Logging in with Google...');
    try {
      console.log('🔐 Sending to backend:', {
        code: googleResponse.code.substring(0, 20) + '...',
        redirect_uri: redirectUri
      });

      const res = await apiClient.post('/auth/google/', {
        code: googleResponse.code,
        redirect_uri: redirectUri,
      });

      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      
      toast.success('Logged in successfully!', { id: toastId });
      navigate('/app/dashboard');

    } catch (err) {
      console.error('❌ Google login error:', err.response?.data || err);
      const errorMessage = err.response?.data?.error || 
                          err.response?.data?.details?.error_description ||
                          err.response?.data?.non_field_errors?.[0] || 
                          'Google login failed. Please try again.';
      toast.error(errorMessage, { id: toastId });
    }
  };

  const login = useGoogleLogin({
    onSuccess: handleLogin,
    onError: (err) => {
      console.error('❌ Google OAuth error:', err);
      toast.error('Google login failed. Please try again.');
    },
    flow: 'auth-code',
  });

  return (
    <button
      onClick={() => login()}
      type="button"
      className="w-full py-2.5 px-4 border border-gray-300 rounded-lg flex items-center justify-center gap-2 hover:bg-black/40 transition-colors"
    >
      <img 
        src="https://www.svgrepo.com/show/475656/google-color.svg" 
        alt="Google" 
        className="w-5 h-5" 
      />
      <span className="text-white/70 font-medium">Sign in with Google</span>
    </button>
  );
}