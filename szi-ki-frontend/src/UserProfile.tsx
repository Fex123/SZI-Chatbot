import React, { Component } from 'react';


const profileSvg = (
    <svg className="profile-svg" height="30px" width="30px" fill="none" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 45.532 45.532" xmlSpace="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M22.766,0.001C10.194,0.001,0,10.193,0,22.766s10.193,22.765,22.766,22.765c12.574,0,22.766-10.192,22.766-22.765 S35.34,0.001,22.766,0.001z M22.766,6.808c4.16,0,7.531,3.372,7.531,7.53c0,4.159-3.371,7.53-7.531,7.53 c-4.158,0-7.529-3.371-7.529-7.53C15.237,10.18,18.608,6.808,22.766,6.808z M22.761,39.579c-4.149,0-7.949-1.511-10.88-4.012 c-0.714-0.609-1.126-1.502-1.126-2.439c0-4.217,3.413-7.592,7.631-7.592h8.762c4.219,0,7.619,3.375,7.619,7.592 c0,0.938-0.41,1.829-1.125,2.438C30.712,38.068,26.911,39.579,22.761,39.579z"></path> </g> </g></svg>
    );
    

interface ProfilePicState {
  isModalOpen: boolean;
}

class ProfilePic extends Component<{}, ProfilePicState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      isModalOpen: false,
    };
  }

  toggleModal = () => {
    this.setState((prevState) => ({
      isModalOpen: !prevState.isModalOpen,
    }));
  };

  
    
  // Change Modal display, make it absolute in the top left. Or something idk, figure it out
  render() {
    return (
      <div>
        <div className="profile-pic-circle" onClick={this.toggleModal}>
          {profileSvg}
        </div>
        {this.state.isModalOpen && (
          
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={this.toggleModal}>&times;</span>
              <p>Modal content goes here...</p>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default ProfilePic;