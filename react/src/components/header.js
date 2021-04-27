import logo from '../img/bank.svg';
//https://codesandbox.io/s/vvoqvk78?from-embed=&file=/components/FullRoster.js
//https://codesandbox.io/s/vvoqvk78?from-embed=&file=/components/Main.js
import { Link } from 'react-router-dom';
import React from 'react';

import { pageSearch } from './js/search.js';

class SignUp extends React.Component {

    isLoggedIn() {
        return localStorage.getItem('isLoggedIn');
    }

    Logout(event){
        event.preventDefault();

        let requestOptions = {
            method: 'POST',
            headers: { 
                //'Content-Type': 'application/json' ,
                'sessionId': localStorage.getItem('sessionId'),
                },
        }

        fetch("http://127.0.0.1:5000/Logout", requestOptions)
        .then(res => res.json())
        .then((data) => {
            if (data.Result == "Success") {
                localStorage.setItem('isLoggedIn', false);
                localStorage.setItem("sessionId", "");
                localStorage.clear();
                window.location.href = '/';
            } else {
                alert('Logout Failed: ' + data.Result);
            }
        })
        .catch(console.log)

        //window.location.href = '/sign-in';
    }

    render() {
        if (!this.isLoggedIn()) {
            return (
                <div>
                    <Link id="sign-up" to="./sign-in" style={{ float: "right" }}>Sign Up</Link>
                    <Link to='/sign-in' id="sign-in" style={{ float: "right" }}>Sign In</Link>
                </div>

            );
        } else {
            return (
                <div>
                    <button id="logout" onClick={this.Logout} style={{ float: "right" }}>Log out</button>
                </div>
            );
        }
    }
}

function Header() {

    return (
        <div>
            <header className="page-header">
                <div className="logo"><img src={logo} alt="logo" /></div>
                <div className="title-text">Picture Bank</div>
                <SignUp />
                <div id="header-search">
                    <input id="top-search" type="text" autoCapitalize="none" placeholder="Search.." onKeyUp={pageSearch} />
                </div>
            </header>
            <div className="header-space"></div>
        </div>
    );
}

function Footer() {
    return (
        <div>
            <div className="footer">
                <div>About</div>
                <div>About2</div>
                <div>About3</div>
            </div>
            <div className="footer-space"></div>
        </div>
    );
}


export {
    Header,
    Footer,
}