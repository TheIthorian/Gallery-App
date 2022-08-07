import React from 'react';

import './js/page-load.js';
import './js/search.js';

import { Header } from './header.js';
import { GalleryPage, ImageModal } from './gallery.js';

class Home extends React.Component {
    render() {
        localStorage.setItem('isPopupOpen', false);
        return (
            <div className='page-container'>
                <Header />
                <GalleryPage />
                <ImageModal />
            </div>
        );
    }
}

export default Home;
