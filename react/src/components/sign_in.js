import React, { useState } from 'react';
import { render } from 'react-dom';
import {Redirect} from 'react-router-dom';

import "../style/sign_in.css";

const settings = {
    hostURL: "http://127.0.0.1:5000/",
}

let link = "";

// dec2hex :: Integer -> String
// i.e. 0-255 -> '00'-'ff'
function dec2hex (dec) {
    return dec.toString(16).padStart(2, "0")
  }
  
  // generateId :: Integer -> String
  function generateId (len) {
    var arr = new Uint8Array((len || 40) / 2)
    window.crypto.getRandomValues(arr)
    return Array.from(arr, dec2hex).join('')
  }

console.log(localStorage.getItem("isLoggedIn"));



function SignIn() {



    let email, password;
    let login = false;
  
    function validateForm() {
        //console.log(email.length, password.length);
        return true;
        return email.length > 0 && password.length > 5;
    }

    function toggleSignIn(props) {
        props.login = !props.login;
        console.log(login);
    }
  
    function handleChangeEmail(e) {
        email = e.target.value;
        validateForm();
    }

    function handleChangePass(e) {
        password = e.target.value;
        validateForm();
    }

    function handleSubmitSignIn(event) {
        if (!email || !password) {
            return;
        }
        event.preventDefault();

        let potentialSessionId = generateId();
        if (localStorage.getItem('sessionId')) {
            potentialSessionId = localStorage.getItem('sessionId');
        }

        let sessionId = potentialSessionId;

        console.log(sessionId);

        let requestOptions = {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' ,
                'sessionId': sessionId,
                },
            body: JSON.stringify({
                Email: email,
                Password: password
            })
        }

        console.log(requestOptions.body);

        fetch("http://127.0.0.1:5000/Login", requestOptions)
        .then(res => res.json())
        .then((data) => {
          console.log(data);
            if (data.Result == "Success") {
              localStorage.setItem('sessionId', sessionId);
              localStorage.setItem('isLoggedIn', true);
              alert('Login Successful')
              error.type = "";
              error.display = false;
              error.wording = "";
              window.location.href = '/';
          } else {
              error.type = "warning";
              error.display = true;
              error.wording = data.Result;
              updateError();
              alert('Login Failed: ' + error.wording);
          }
        })
        .catch(console.log); 
                
      }

    function handleSubmitSignUp(event) {
        event.preventDefault();

        let potentialSessionId = generateId();
        if (localStorage.getItem('sessionId')) {
            potentialSessionId = localStorage.getItem('sessionId');
        }

        let sessionId = potentialSessionId;

        console.log(sessionId);

        let requestOptions = {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' ,
                'sessionId': sessionId,
                },
            body: JSON.stringify({
                Email: email,
                Password: password
            })
        }

        console.log(requestOptions.body);

        fetch("http://127.0.0.1:5000/Register", requestOptions)
        .then(res => res.json())
        .then((data) => {
          console.log(data);
            if (data.Result == "Success") {
              localStorage.setItem('sessionId', sessionId);
              localStorage.setItem('isLoggedIn', true);
              alert('Login Successful')
              window.location.href = '/';
          } else {
              alert('Login Failed: ' + data.Result);
          }
        })
        .catch(console.log)

        
      }

    const error = {
        type : "",
        display: false,
        wording : ""
    };

    
    function updateError() {  
        let Errormessage = document.getElementById("ErrorMessage");      
        Errormessage.class = "error-message " + error.type;
        Errormessage.hidden = !error.display;
        Errormessage.innerText = error.wording;
    }

    return (
        <div className="background">
            <div className="parent-container" >
                <div className="input-box">
                    <h1 className="title">Intraspace</h1>
                    <h2 className="title">Welcome Back!</h2>
                    <form onSubmit={handleSubmitSignIn} className="login-from">
                        <div className="input-group">
                            <label for="email">Email: </label>
                            <input name="email" type="text" className="singup-input" onChange={handleChangeEmail} />
                        </div>
                        <div className="input-group">
                            <label for="password">Password: </label>
                            <input name="password" type="password" className="singup-input" onChange={handleChangePass} />
                        </div>
                        <button type="submit" disabled={!validateForm()} className="form-submit">
                            Sign In
                        </button>
                    </form>
                    <a href={link} id="homelink" hidden="true">Home</a>
                    <p>Don't have an account? <button className="toggle-signin" onClick={handleSubmitSignUp}>Create one</button></p>
                    <p id="ErrorMessage" hidden="true" className="error-message"></p>
                </div>
            </div>
        </div>
        
    );
}

export default SignIn;

