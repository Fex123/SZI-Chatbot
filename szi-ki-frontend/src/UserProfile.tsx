import React, { Component } from 'react';
import './App.css';
import { logoutUser } from './helper';
import { useNavigate } from 'react-router-dom';

const profileSvg = (
  <svg className="profile-svg" height="30px" width="30px" fill="none" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 45.532 45.532" xmlSpace="preserve">
    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
    <g id="SVGRepo_iconCarrier">
      <g>
        <path d="M22.766,0.001C10.194,0.001,0,10.193,0,22.766s10.193,22.765,22.766,22.765c12.574,0,22.766-10.192,22.766-22.765 S35.34,0.001,22.766,0.001z M22.766,6.808c4.16,0,7.531,3.372,7.531,7.53c0,4.159-3.371,7.53-7.531,7.53 c-4.158,0-7.529-3.371-7.529-7.53C15.237,10.18,18.608,6.808,22.766,6.808z M22.761,39.579c-4.149,0-7.949-1.511-10.88-4.012 c-0.714-0.609-1.126-1.502-1.126-2.439c0-4.217,3.413-7.592,7.631-7.592h8.762c4.219,0,7.619,3.375,7.619,7.592 c0,0.938-0.41,1.829-1.125,2.438C30.712,38.068,26.911,39.579,22.761,39.579z"></path>
      </g>
    </g>
  </svg>
);

const signoutSvg = (
  <svg viewBox="0 0 24 24" fill="none" height="24px" width="24px" xmlns="http://www.w3.org/2000/svg" className="modal-svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M4 5.4A1.4 1.4 0 0 1 5.4 4h6.2A1.4 1.4 0 0 1 13 5.4V8a1 1 0 1 0 2 0V5.4A3.4 3.4 0 0 0 11.6 2H5.4A3.4 3.4 0 0 0 2 5.4v13.2A3.4 3.4 0 0 0 5.4 22h6.2a3.4 3.4 0 0 0 3.4-3.4V16a1 1 0 1 0-2 0v2.6a1.4 1.4 0 0 1-1.4 1.4H5.4A1.4 1.4 0 0 1 4 18.6V5.4Z" ></path><path d="M17.293 8.293a1 1 0 0 1 1.414 0l3 3a1 1 0 0 1 0 1.414l-3 3a1 1 0 0 1-1.414-1.414L18.586 13H7a1 1 0 1 1 0-2h11.586l-1.293-1.293a1 1 0 0 1 0-1.414Z" ></path></g></svg>
);

interface ProfilePicState {
  isModalOpen: boolean;
  username: string;
}

class ProfilePic extends Component<{}, ProfilePicState> {
  modalRef: React.RefObject<HTMLDivElement>;
  navigate: ReturnType<typeof useNavigate>;

  constructor(props: {}) {
    super(props);
    this.state = {
      isModalOpen: false,
      username: ''
    };
    this.modalRef = React.createRef();
    this.navigate = useNavigate();
  }

  componentDidMount() {
    document.addEventListener('mousedown', this.handleClickOutside);
    const loginResponse = sessionStorage.getItem('loginResponse');
    if (loginResponse) {
      const { username } = JSON.parse(loginResponse);
      this.setState({ username });
    }
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  toggleModal = () => {
    this.setState((prevState) => ({
      isModalOpen: !prevState.isModalOpen,
    }));
  };

  handleClickOutside = (event: MouseEvent) => {
    if (this.modalRef.current && !this.modalRef.current.contains(event.target as Node)) {
      this.setState({ isModalOpen: false });
    }
  };

  handleLogout = async () => {
    try {
      await logoutUser();
      sessionStorage.removeItem('loginResponse');
      this.navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  render() {
    return (
      <div>
        <div className="profile-pic-circle" onClick={this.toggleModal}>
          {profileSvg}
        </div>
        {this.state.isModalOpen && (
          <div className="user-modal" ref={this.modalRef}>
            <div className="modal-content">
              <div className="modal-user-info">
                {this.state.username}
              </div>
              <div style={{ border: '1px solid #acacac', margin: '10px 0' }}></div>
              <div className="modal-button" onClick={this.handleLogout}>
                {signoutSvg}
                <div className="signout-text">
                  Abmelden
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default ProfilePic;