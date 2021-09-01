import React from "react";

class Popup extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isPopupOpenState : this.props.isPopupOpen
        }
    }


    togglePopup = () => {
        this.setState({isPopupOpenState: !this.state.isPopupOpenState});
        //this.props.isPopupOpen = this.state.isPopupOpenState;
    }

    render() {
        let {content, isPopupOpen, handleClose} = this.props;
        let {isPopupOpenState} = this.state;
        if (isPopupOpen) {
            return (
                <div key={this.props.isPopupOpen} className="popup-box">
                    <div className="box">
                        <button className="close-icon custom" onClick={handleClose}>x</button>
                        {content}
                    </div>
                </div>
            );
        } else {
            return (<></>);
        }
    }
};

export default Popup;