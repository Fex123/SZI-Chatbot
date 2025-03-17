import React, { Component } from 'react';
import './App.css';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';
import { loginUser, registerUser } from './helper';



interface LoginState {
  email: string;
  password: string;
  confirmPassword: string;
  darkMode: boolean;
  isLogin: boolean;
  feedbackMessage: string;
}

class Login extends Component<{}, LoginState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      email: '',
      password: '',
      confirmPassword: '',
      darkMode: false,
      isLogin: true,
      feedbackMessage: '',
    };
  }

  handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    this.setState({ [name]: value } as unknown as Pick<LoginState, keyof LoginState>);
  };

  handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const { email, password, confirmPassword, isLogin } = this.state;

    if (isLogin) {
      try {
        const response = await loginUser(email, password);
        console.log('Login successful:', response);
        // Save login response to session storage
        sessionStorage.setItem('loginResponse', JSON.stringify(response));
        // Handle successful login
        window.location.href = 'app.html'; // Redirect to app.html
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
        this.setState({
          isLogin: true,
          feedbackMessage: 'Erfolgreich registriert!',
        });
      } catch (error) {
        console.error('Registration failed:', error);
        // Handle registration error
      }
    }
  };

  toggleDarkMode = () => {
    this.setState((prevState) => ({ darkMode: !prevState.darkMode }));
  };

  toggleLoginState = () => {
    this.setState((prevState) => ({ isLogin: !prevState.isLogin, feedbackMessage: '' }));
  };

  render() {
    const { email, password, confirmPassword, darkMode, isLogin, feedbackMessage } = this.state;

    return (
      <div className={`login-container ${darkMode ? 'dark' : ''}`}>
        <div className="login-top-bar">
          <DarkModeToggle isDark={darkMode} toggleDarkMode={this.toggleDarkMode} />
        </div>
        <div className="login-logo">
          <img src={logo} alt="Logo" className="dhbw-logo" title="Create new chat" />
          <h1>SZI Assistent</h1>
        </div>
        <form className="login-form" onSubmit={this.handleSubmit}>
          <h1>{isLogin ? ("Anmelden") : ("Registrieren")}</h1>
          {feedbackMessage && <p className="feedback-message">{feedbackMessage}</p>}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={this.handleInputChange}
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
              onChange={this.handleInputChange}
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
                onChange={this.handleInputChange}
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
              <a onClick={this.toggleLoginState} className="forgot-password">Noch keinen Account? Registrieren</a>
            </div>
          ) : (
            <div className="form-group">
              <a onClick={this.toggleLoginState} className="forgot-password">Bereits registriert? Anmelden</a>
            </div>
          )}
        </form>
      </div>
    );
  }
}

export default Login;