import React, { useState } from 'react';
import './App.css';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';
import { loginUser, registerUser } from './helper';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    if (name === 'email') setEmail(value);
    if (name === 'password') setPassword(value);
    if (name === 'confirmPassword') setConfirmPassword(value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (isLogin) {
      try {
        const response = await loginUser(email, password);
        console.log('Login successful:', response);
        // Save login response to session storage
        sessionStorage.setItem('loginResponse', JSON.stringify(response));
        // Handle successful login
        navigate('/app'); // Redirect to the main app
      } catch (error) {
        console.error('Login failed:', error);
        // Handle login error
      }
    } else {
      if (password !== confirmPassword) {
        console.log('Passwords do not match');
        // Handle error
        return;
      }
      try {
        const response = await registerUser(email, password, email); // Assuming display name is the same as email
        console.log('Registration successful:', response);
        // Handle successful registration
        setIsLogin(true);
        setFeedbackMessage('Erfolgreich registriert!');
        navigate('/app'); // Redirect to the main app after registration
      } catch (error) {
        console.error('Registration failed:', error);
        // Handle registration error
      }
    }
  };

  const toggleDarkMode = () => {
    setDarkMode((prevDarkMode) => !prevDarkMode);
  };

  const toggleLoginState = () => {
    setIsLogin((prevIsLogin) => !prevIsLogin);
    setFeedbackMessage('');
  };

  return (
    <div className={`login-container ${darkMode ? 'dark' : ''}`}>
      <div className="login-top-bar">
        <DarkModeToggle isDark={darkMode} toggleDarkMode={toggleDarkMode} />
      </div>
      <div className="login-logo">
        <img src={logo} alt="Logo" className="dhbw-logo" title="Create new chat" />
        <h1>SZI Assistent</h1>
      </div>
      <form className="login-form" onSubmit={handleSubmit}>
        <h1>{isLogin ? 'Anmelden' : 'Registrieren'}</h1>
        {feedbackMessage && <p className="feedback-message">{feedbackMessage}</p>}
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Passwort</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={handleInputChange}
            required
          />
        </div>
        {!isLogin && (
          <div className="form-group">
            <label htmlFor="confirmPassword">Passwort bestätigen</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={confirmPassword}
              onChange={handleInputChange}
              required
            />
          </div>
        )}
        <div className="form-group">
          <a href="#" className="forgot-password">Passwort vergessen?</a>
        </div>

        {isLogin ? (
          <div className="form-group">
            <button type="submit" className="login-register-button">Anmelden</button>
          </div>
        ) : (
          <div className="form-group">
            <button type="submit" className="login-register-button">Registrieren</button>
          </div>
        )}
        {isLogin ? (
          <div className="form-group">
            <a onClick={toggleLoginState} className="forgot-password">Noch keinen Account? Registrieren</a>
          </div>
        ) : (
          <div className="form-group">
            <a onClick={toggleLoginState} className="forgot-password">Bereits registriert? Anmelden</a>
          </div>
        )}
      </form>
    </div>
  );
};

export default Login;