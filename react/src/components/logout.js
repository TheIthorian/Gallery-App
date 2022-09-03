// Logs user out of current session and changes location

import { API_URL } from './constants';

// ** Unused **
function Logout() {
    let sessionId = localStorage.getItem('sessionId');

    let requestOptions = {
        method: 'POST',
        headers: {
            sessionId: sessionId,
        },
        body: { Data: 'Data' },
    };

    console.log(requestOptions.sessionId);

    fetch(API_URL + '/Logout', requestOptions)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            if (data.Result == 'Success') {
                localStorage.setItem('isLoggedIn', false);
                requestOptions.localStorage.setItem('sessionId', '');
                alert('Logout Successful');
                window.location.href = '/';
            } else {
                alert('Logout Failed: ' + data.Result);
            }
        })
        .catch(console.log);

    return <></>;
}

export default Logout;
