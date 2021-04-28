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
    let createAccount = false;
  
    function validateForm() {
        
        if (!email || !password) {return false;}
        else {return email.length > 0 && password.length > 4;}     
    }

    function toggleSignIn(props) {
        props.login = !props.login;
        console.log(login);
    }
  
    function handleChangeEmail(e) {
        email = e.target.value;
        //validateForm();
    }

    function handleChangePass(e) {
        password = e.target.value;
        validateForm();
    }

    function handleSubmitSignIn(event) {
        
        event.preventDefault();

        if (!email || !password) {
            error.wording = "Please provide an email and password";
            error.display = true;
            error.type = "warning"
            updateError();
            return;
        }
        

        let potentialSessionId = generateId();
        if (localStorage.getItem('sessionId')) {
            potentialSessionId = localStorage.getItem('sessionId');
        }

        let sessionId = potentialSessionId;

        //console.log(sessionId);

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

        //console.log(requestOptions.body);

        fetch("http://127.0.0.1:5000/Login", requestOptions)
        .then(res => res.json())
        .then((data) => {
          console.log(data);
            if (data.Result == "Success") {
              localStorage.setItem('sessionId', sessionId);
              localStorage.setItem('isLoggedIn', true);
              error.type = "";
              error.display = false;
              error.wording = "";
              window.location.href = '/';
          } else {
              error.type = "warning";
              error.display = true;
              error.wording = data.Result;
              updateError();
              //alert('Login Failed: ' + error.wording);
          }
        })
        .catch(console.log); 
                
      }

    function handleSubmitSignUp(event) {
        event.preventDefault();

        if (!email || !password) {
            return;
        }

        if (password.lenght < 5) {
            error.wording = "Password must be at least 5 characters long";
            error.display = true;
            error.type = "warning"
            return;
        }

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
              //alert('Login Successful')
              window.location.href = '/';
          } else {
            error.wording = data.Result;
            error.display = true;
            error.type = "warning"
            updateError();
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

    function toggleSignUp () {
        console.log(createAccount);

        if (createAccount) {
            document.getElementById("sign-up-link").style.display = 'block';
            document.getElementById("create-account-action").style.display = 'none';

            document.getElementById("sign-in-link").style.display = 'none';
            document.getElementById("sign-in-action").style.display = 'block';
        }
        if (!createAccount) {
            document.getElementById("sign-up-link").style.display = 'none';
            document.getElementById("create-account-action").style.display = 'block';
            document.getElementById("sign-in-link").style.display = 'block';
            document.getElementById("sign-in-action").style.display = 'none';
        }
        createAccount = !createAccount;
        return;

    }

    return (
        <div className="background">
            <div className="parent-container" >
                <div className="input-box">
                    <h1 className="title">Picture Bank</h1>
                    <form //onSubmit={handleSubmitSignIn} 
                    className="login-from" method="POST">
                        <div className="input-group">
                            <label for="email">Email: </label>
                            <input name="email" type="text" className="singup-input" onChange={handleChangeEmail} />
                        </div>
                        <div className="input-group">
                            <label for="password">Password: </label>
                            <input name="password" type="password" className="singup-input" onChange={handleChangePass} />
                        </div>
                        <button id="sign-in-action" type="submit" className="form-submit" onClick={handleSubmitSignIn}>
                            Sign In
                        </button>
                        <button id="create-account-action" type="submit" className="form-submit" onClick={handleSubmitSignUp}>
                            Create Account
                        </button>
                    </form>
                    <a href={link} id="homelink" hidden="true">Home</a>
                    <p id="sign-up-link">Don't have an account? <button className="toggle-signin" onClick={toggleSignUp}>Create one</button></p>
                    <p id="sign-in-link">Already have an account? <button className="toggle-signin" onClick={toggleSignUp}>Sign in</button></p>
                    <p id="ErrorMessage" hidden="true" className="error-message"></p>
                </div>
            </div>
        </div>
        
    );
}

export default SignIn;

