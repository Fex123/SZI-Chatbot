import React, { useState } from 'react';
import './App.css';
import logo from './assets/logo.svg';
import { loginUser, registerUser } from './helper';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
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
        sessionStorage.removeItem('loginResponse-plaiooijdjfpakij103978128739807298312');
        sessionStorage.setItem('loginResponse-plaiooijdjfpakij103978128739807298312', JSON.stringify(response));

        navigate('/app');
      } catch (error) {
        console.error('Login failed:', error);
        setErrorMessage('Login fehlgeschlagen. ' + error);
      }
    } else {
      if (password !== confirmPassword) {
        setErrorMessage("Passwörter stimmen nicht überein.");
        return;
      }
      try {
        const response = await registerUser(email, password, email);
        console.log('Registration successful:', response);

        setIsLogin(true);
        setErrorMessage('Erfolgreich registriert!');
      } catch (error) {
        console.error('Registration failed:', error);
        setErrorMessage('Registration fehlgeschlagen. ' + error);
      }
    }
  };

  const toggleLoginState = () => {
    setIsLogin((prevIsLogin) => !prevIsLogin);
  };

  return (
    <div className={`login-container ${darkMode ? 'dark' : ''}`}>
      <div className="login-top-bar">
        {/*<DarkModeToggle isDark={darkMode} toggleDarkMode={toggleDarkMode} />*/}
      </div>
      <div className="login-logo">
        <img src={logo} alt="Logo" className="dhbw-logo" title="Create new chat" />
        <h1>SZI Assistent</h1>
      </div>
      <form className="login-form" onSubmit={handleSubmit}>
        <h1>{isLogin ? 'Anmelden' : 'Registrieren'}</h1>
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
        {/*
        <div className="form-group">
          <a href="#" className="forgot-password">Passwort vergessen?</a>
        </div>
        */
        }
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
      {errorMessage !== "" ? (

        <div className="error-message">

          {errorMessage}

        </div>) : null}
    </div>
  );
};

export default Login;