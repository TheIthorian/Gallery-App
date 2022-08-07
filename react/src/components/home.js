import React from 'react';
import ScriptTag from 'react-script-tag';

import './js/page-load.js';
import './js/search.js';

import { Header } from './header.js';
import { GalleryPage, ImageModal } from './gallery.js';

class Head extends React.Component {
    render() {
        return (
            <head>
                <title>Picture Bank</title>
                <meta name='viewport' content='width=device-width, initial-scale=1' />
                <link rel='stylesheet' href='./style/style.css' />
            </head>
        );
    }
}

class Home extends React.Component {
    render() {
        localStorage.setItem('isPopupOpen', false);
        return (
            <>
                <Head />
                <div className='page-container'>
                    <Header />
                    <GalleryPage />
                    <ImageModal />
                    {/* <Footer /> */}
                    <ScriptTag type='text/javascript' src='./js/page-load.js' />
                </div>
            </>
        );
    }
}

export default Home;
