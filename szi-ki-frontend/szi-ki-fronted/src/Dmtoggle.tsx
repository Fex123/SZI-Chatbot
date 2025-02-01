import { Component } from 'react';

interface DarkModeToggleProps {
  isDark: boolean;
  toggleDarkMode: () => void;
}

interface DarkModeToggleState {
  isDark: boolean;
}

class DarkModeToggle extends Component<DarkModeToggleProps, DarkModeToggleState> {

  constructor(props: DarkModeToggleProps) {
    super(props);
    this.state = {
      isDark: props.isDark
    };
  }

  toggleDarkMode = () => {
    this.setState({ isDark: !this.state.isDark }, () => {
      this.props.toggleDarkMode();
    });
  };

  render() {
    return (
      <button className="dark-mode-button" onClick={this.toggleDarkMode}>
        <svg className="dark-mode-svg" width="24px" height="24px" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path className="dark-mode-path" d="M0 8.00002C0 4.75562 1.93132 1.9623 4.70701 0.707031L5.65436 1.65438C5.2352 2.51383 5 3.47946 5 4.50002C5 8.08987 7.91015 11 11.5 11C12.5206 11 13.4862 10.7648 14.3456 10.3457L15.293 11.293C14.0377 14.0687 11.2444 16 8 16C3.58172 16 0 12.4183 0 8.00002Z" />
          <path className="dark-mode-path" d="M11.5 7.00003L9 4.50003L11.5 2.00003L14 4.50003L11.5 7.00003Z" />
        </svg>
      </button>
    );
  }
}

export default DarkModeToggle;