import React, { Component } from 'react';
import './App.css';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';

interface LoginState {
  email: string;
  password: string;
  confirmPassword: string;
  darkMode: boolean;
  isLogin: boolean;
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
    };
  }

  handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    this.setState({ [name]: value } as unknown as Pick<LoginState, keyof LoginState>);
  };

  handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (this.state.isLogin === true) {
      console.log('Login:', this.state.email, this.state.password);
    } else {
      if (this.state.password !== this.state.confirmPassword) {
        console.log('Passwords do not match');
        return;
      }
      console.log('Register:', this.state.email, this.state.password);
    }
  };

  toggleDarkMode = () => {
    this.setState((prevState) => ({ darkMode: !prevState.darkMode }));
  };

  toggleLoginState = () => {
    this.setState((prevState) => ({ isLogin: !prevState.isLogin }));
  };

  render() {
    const { email, password, confirmPassword, darkMode, isLogin } = this.state;

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