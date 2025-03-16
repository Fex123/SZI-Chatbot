import React, { Component } from 'react';
import './App.css';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';

interface LoginState {
  email: string;
  password: string;
  darkMode: boolean;
}

class Login extends Component<{}, LoginState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      email: '',
      password: '',
      darkMode: false,
    };
  }

  handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    this.setState({ [name]: value } as unknown as Pick<LoginState, keyof LoginState>);
  };

  handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Handle login logic here
  };

  toggleDarkMode = () => {
    this.setState((prevState) => ({ darkMode: !prevState.darkMode }));
  };

  render() {
    const { email, password, darkMode } = this.state;

    return (
      <div className={`login-container ${darkMode ? 'dark' : ''}`}>
        <div className="login-top-bar">
          <DarkModeToggle isDark={darkMode} toggleDarkMode={this.toggleDarkMode} />
        </div>
        <div className="login-logo">
        <img src={logo} alt="Logo" className="dhbw-logo" title="Create new chat"/>
          <h1>SZI Assistent</h1>
        </div>
        <form className="login-form" onSubmit={this.handleSubmit}>
          <h1>Login</h1>
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
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={this.handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <a href="#" className="forgot-password">Password vergessen?</a>
          </div>
          <div className="form-group">
            <button type="submit" className="login-button">Login</button>
          </div>
          <div className="form-group">
            <button type="button" className="register-button">Register</button>
          </div>
        </form>
      </div>
    );
  }
}

export default Login;