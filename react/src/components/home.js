import React from 'react';
import ScriptTag from 'react-script-tag';

import './js/page-load.js';
import './js/search.js';

import {Header, Footer} from './header.js';
import {GalleryPage, ImageModal} from './gallery.js';


class Head extends React.Component {
    render(){
        return (
            <head>
                <title>Gallery</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="stylesheet" href="./style/style.css" />
            </head>
        );
    }
}

class Home extends React.Component {
    
    render(){
        localStorage.setItem("isPopupOpen", false);
        return (
            <div>
                <Header />
                <GalleryPage />
                <ImageModal />
                {/* <Footer /> */}
                <ScriptTag type="text/javascript" src="./js/page-load.js" />
            </div>
        );
    }
}

export default Home;