import React from 'react';
import Popup from './popup.js';

import editIcon from '../img/edit.svg';
import addIcon from '../img/add.svg';
import removeIcon from '../img/remove.svg';

import sizeSmall from '../img/size-small.svg';
import sizeLarge from '../img/size-large.svg';
import { API_URL } from './constants.js';

const settings = {
    hostURL: API_URL + '/',
};

class ImageSizeCheckbox extends React.Component {
    constructor(props) {
        super(props);
        this.active = true;
    }

    handleClick = () => {
        let scale = this.active ? 1 : 2;

        let imgLeft = document.getElementsByClassName('image-size-toggle')[0].childNodes[0];
        let imgRight = document.getElementsByClassName('image-size-toggle')[0].childNodes[2];

        if (scale === 1) {
            imgLeft.classList.remove('active');
            imgRight.classList.add('active');
        } else {
            imgLeft.classList.add('active');
            imgRight.classList.remove('active');
        }

        let galleryImages = document.getElementsByClassName('picture-container');

        for (let j = 0; j < galleryImages.length; j++) {
            galleryImages[j].classList.remove('size1', 'size2');
            galleryImages[j].classList.add('size' + scale);
        }

        let imageTitles = document.getElementsByClassName('title');
        for (let i = 0; i < imageTitles.length; i++) {
            imageTitles[i].style.display = this.active ? 'none' : 'block';
        }

        this.active = !this.active;
    };

    render() {
        return (
            <div className='image-size-toggle'>
                <img className='active' src={sizeLarge} alt='large icons' />
                <label className='switch'>
                    <input
                        type='checkbox'
                        className='image-scale-checkbox'
                        id='image-scale'
                        onClick={this.handleClick}
                    />
                    <span className='slider'></span>
                </label>
                <img src={sizeSmall} alt='small icons' />
            </div>
        );
    }
}

// Class to render image data
class Image extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            imageData: {},
            isPopupOpen: false,

            updateTitle: '',
            updateURL: '',
            updateMessage: '',
        };
    }

    handleClick = () => {
        // Container for modal
        let modal = document.getElementById('selected-image-modal');

        // Modal img element
        let modalImg = document.getElementById('modal-image');

        // Container for image
        let imageContainer = document.getElementById('ImageId:' + this.props.imageData.ImageId);

        // The selected img element
        let image = imageContainer.childNodes[0];

        modal.style.display = 'block';
        modalImg.src = image.src;
        modal.childNodes[1].innerText = image.alt;

        modal.childNodes[2].value = this.props.imageData.ImageId;
        modal.childNodes[3].value = this.props.imageData.ImageId;

        modal.classList.toggle('active');

        // Close button
        var closeButton = modal.childNodes[4];

        // When the user clicks on <span> (x), close the modal
        closeButton.onclick = function () {
            modal.style.display = 'none';
        };
    };

    handleRemoveImage = e => {
        let imageId = e.target.value;
        let requestOptions = {
            method: 'DELETE',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
        };

        fetch(
            settings.hostURL +
                'Gallery/' +
                this.props.imageData.GalleryId +
                '/RemoveImage/' +
                imageId,
            requestOptions
        )
            .then(res => res.json())
            .then(data => {
                // console.log(data);
                if (data.Result === 'Success') {
                    document.getElementById('ImageId:' + imageId).style.display = 'none';
                } else {
                    console.log('Error removing image');
                }
            })
            .catch(console.log);
    };

    handleEditImage = () => {
        if (this.state.updateTitle.length === 0) {
            this.setState({ updateMessage: 'The title cannot be empty' });
            return;
        }
        if (this.state.updateURL.length === 0) {
            this.setState({ updateMessage: 'The URL cannot be empty' });
            return;
        }

        let imageId = this.props.imageData.ImageId;

        let requestOptions = {
            method: 'POST',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Title: this.state.updateTitle,
                URL: this.state.updateURL,
            }),
        };

        fetch(
            settings.hostURL +
                'Gallery/' +
                this.props.imageData.GalleryId +
                '/Image/' +
                imageId +
                '/Update',
            requestOptions
        )
            .then(res => res.json())
            .then(data => {
                // console.log(data);
                if (data.Result === 'Success') {
                    let selectedImage = document.getElementById('ImageId:' + imageId);
                    selectedImage.childNodes[1].childNodes[1].innerText = data.Message.Title;
                    selectedImage.childNodes[0].src = data.Message.URL;
                    this.setState({
                        isPopupOpen: false,
                    });
                } else {
                    console.log('Error updating image');
                }
            })
            .catch(console.log);
    };

    togglePopup = () => {
        this.setState({
            isPopupOpen: !this.state.isPopupOpen,
            updateTitle: this.props.imageData.Title,
            updateURL: this.props.imageData.URL,
        });
    };

    handleOnChange = e => {
        let Title;
        let URL;

        if (e.target.name === 'URL') {
            URL = e.target.value;
            this.setState({ updateURL: URL });
        }
        if (e.target.name === 'Title') {
            Title = e.target.value;
            this.setState({ updateTitle: Title });
        }
    };

    render() {
        const { imageData } = this.props;
        const { isPopupOpen, updateMessage } = this.state;
        let hidden = imageData.hidden ? 'hidden' : '';
        let containerClass = `picture-container size2 ${hidden}`;
        return (
            <div
                value={imageData.ImageId}
                id={'ImageId:' + imageData.ImageId}
                className={containerClass}
            >
                <img
                    loading='lazy'
                    onClick={this.handleClick}
                    className='gallery-image'
                    src={
                        imageData.Image
                            ? `data:image/png;base64, ${imageData.Image}`
                            : imageData.URL
                    }
                    alt={imageData.Title}
                />
                <span className='title'>
                    <input
                        type='image'
                        src={removeIcon}
                        value={imageData.ImageId}
                        onClick={this.handleRemoveImage}
                        className='left'
                        alt='remove'
                    />
                    <span className='title-text'>{imageData.Title}</span>
                    <input
                        type='image'
                        src={editIcon}
                        value={imageData.ImageId}
                        onClick={this.togglePopup}
                        className='right'
                        alt='edit'
                    />
                </span>
                <Popup
                    key='UpdateImage'
                    handleClose={this.togglePopup}
                    isPopupOpen={isPopupOpen}
                    content={
                        <>
                            <h3>Edit Image:</h3>
                            <div className='input-group'>
                                <label htmlFor='Title'>Title: </label>
                                <input
                                    maxLength='45'
                                    onChange={this.handleOnChange}
                                    name='Title'
                                    defaultValue={imageData.Title}
                                    required
                                />
                            </div>
                            <div className='input-group'>
                                <label htmlFor='URL'>URL: </label>
                                <input
                                    maxLength='3200'
                                    onChange={this.handleOnChange}
                                    name='URL'
                                    defaultValue={imageData.URL}
                                    required
                                />
                            </div>
                            <p className='error-message left popup'>{updateMessage}</p>
                            <button
                                className='primary'
                                type='submit'
                                onClick={this.handleEditImage}
                            >
                                Save
                            </button>
                            <br />
                        </>
                    }
                />
            </div>
        );
    }
}

// Class to render a gallery and its images
class Gallery extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            imageList: [
                {
                    // "Image": <None>,
                    // "ImageId": Int,
                    // "Title": <String>
                    // "URL": <String>
                },
            ],
            isPopupOpen: false,
            AddImageTitle: '',
            AddImageURL: '',
            AddImageMessage: '',

            UpdateGalleryMessage: '',
            isUpdatePopupOpen: false,
            UpdateGalleryTitle: '',

            RemoveGalleryMessage: '',
            isRemovePopupOpen: false,

            galleryTitle: this.props.galleryData.Title,
            oldGalleryTitle: this.props.galleryData.Title,
        };
        this.isGalleryOpen = false;
        this.galleryId = props.galleryData.GalleryId;
    }

    componentDidMount() {
        const { galleryData } = this.props;
        this.getGalleryImages(galleryData.GalleryId);
    }

    getGalleryImages(GalleryId) {
        let requestOptions = {
            method: 'GET',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
        };

        fetch(settings.hostURL + 'Gallery/' + GalleryId + '/Images', requestOptions)
            .then(res => res.json())
            .then(data => {
                if (data.Result === 'Success') {
                    for (const message of data.Message) {
                        message.hidden = true;
                    }
                    // console.log(data.Message);
                    this.setState({ imageList: data.Message });
                } else {
                    this.setState({ imageList: null });
                }
            })
            .catch(console.log);
    }

    togglePopup = () => {
        this.setState({
            isPopupOpen: !this.state.isPopupOpen,
            AddImageMessage: '',
            AddImageTitle: '',
            AddImageURL: '',
        });
    };

    toggleUpdatePopup = () => {
        this.setState({
            isUpdatePopupOpen: !this.state.isUpdatePopupOpen,
            UpdateGalleryMessage: '',
            UpdateGalleryTitle: '',
        });
    };

    toggleRemovePopup = e => {
        this.setState({
            isRemovePopupOpen: !this.state.isRemovePopupOpen,
            RemoveGalleryMessage: '',
        });
    };

    hideGallery() {
        document.getElementById('GalleryId:' + this.galleryId).style.display = 'none';
    }

    handleOnChange = e => {
        let Title;
        let URL;

        if (e.target.name === 'AddImageTitle') {
            Title = e.target.value;
            this.setState({ AddImageTitle: Title });
        }
        if (e.target.name === 'URL') {
            URL = e.target.value;
            this.setState({ AddImageURL: URL });
        }
        if (e.target.name === 'UpdateGalleryTitle') {
            Title = e.target.value;
            this.setState({ galleryTitle: Title });
        }
    };

    handleAddImageSubmit = GalleryId => {
        if (this.state.AddImageTitle.length === 0) {
            this.setState({ AddImageMessage: 'The title cannot be empty' });
            return;
        }
        if (this.state.AddImageURL.length === 0) {
            this.setState({ AddImageMessage: 'The URL cannot be empty' });
            return;
        }
        let requestOptions = {
            method: 'POST',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Title: this.state.AddImageTitle,
                URL: this.state.AddImageURL,
                Image: '',
                PublicImageIndicator: '6',
            }),
        };

        fetch(settings.hostURL + 'Gallery/' + GalleryId + '/AddImage', requestOptions)
            .then(res => res.json())
            .then(data => {
                if (data.Result === 'Success') {
                    // console.log(data);
                    let newImageList = this.state.imageList;
                    let newImage = data.Message;
                    newImage.hidden = false;
                    newImageList.push(newImage);

                    this.setState({
                        isPopupOpen: false,
                        AddImageMessage: 'Image Added sucessfully',
                        imageList: newImageList,
                    });
                } else {
                    this.setState({ AddImageMessage: 'Uanble to add image: ' + data.Result });
                }
            })
            .catch(console.log);

        //const { galleryData } = this.props;
        //this.getGalleryImages(galleryData.GalleryId);
    };

    handleUpdateGallerySubmit = GalleryId => {
        if (this.state.galleryTitle.length === 0) {
            this.setState({ UpdateGalleryMessage: 'The title cannot be empty' });
            return;
        }
        let requestOptions = {
            method: 'POST',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Title: this.state.galleryTitle,
            }),
        };

        fetch(settings.hostURL + 'UpdateGallery/' + GalleryId, requestOptions)
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if (data.Result === 'Success') {
                    for (let i = 0; i < data.Message.length; i++) {
                        // console.log("" + data.Message[i].GalleryId + ":" + this.props.galleryData.GalleryId + ":" + this.galleryId);
                        if (data.Message[i].GalleryId === this.props.galleryData.GalleryId) {
                            this.setState({
                                galleryTitle: data.Message[i].Title,
                                oldGalleryTitle: data.Message[i].Title,
                            });
                        }
                    }

                    this.setState({
                        isUpdatePopupOpen: false,
                    });
                } else {
                    this.setState({
                        UpdateGalleryMessage: 'Uanble to update gallery: ' + data.Result,
                    });
                }
            })
            .catch(console.log);
    };

    handleRemoveGallerySubmit = GalleryId => {
        let requestOptions = {
            method: 'POST',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Title: this.state.galleryTitle,
            }),
        };

        fetch(settings.hostURL + 'RemoveGallery/' + GalleryId, requestOptions)
            .then(res => res.json())
            .then(data => {
                if (data.Result === 'Success') {
                    this.setState({
                        isRemovePopupOpen: false,
                    });
                    this.hideGallery();
                } else {
                    this.setState({
                        RemoveGalleryMessage: 'Uanble to remove gallery: ' + data.Result,
                    });
                }
            })
            .catch(console.log);
    };

    toggleGallery = e => {
        // This should probably run getImages for the gallery so we don't have to load all the images at first

        let content = e.target.parentNode;
        content = content.nextElementSibling;

        let galleryButton = e.target;

        let areGalleryImagesSmall = document.getElementById('image-scale').checked;

        while (content && content.tagName !== 'button') {
            content.childNodes[1].style.display = !areGalleryImagesSmall ? 'block' : 'none';

            if (this.isGalleryOpen) {
                galleryButton.classList.remove('active');

                // Image
                content.classList.add('hidden');
                // Title
                content.childNodes[1].classList.add('hidden');
            } else {
                galleryButton.classList.add('active');
                // content.style.display = 'block';
                // content.style.maxHeight = null;

                //content.childNodes[1].style.maxHeight = '100%';
                content.classList.remove('hidden');
                content.childNodes[1].classList.remove('hidden');
            }
            content = content.nextElementSibling;
        }
        this.isGalleryOpen = !this.isGalleryOpen;
    };

    render() {
        const { galleryData } = this.props;
        let {
            imageList,
            isPopupOpen,
            AddImageMessage,
            isGalleryOpen,
            isUpdatePopupOpen,
            UpdateGalleryMessage,
            galleryTitle,
            oldGalleryTitle,
            isRemovePopupOpen,
            RemoveGalleryMessage,
        } = this.state;
        console.log(imageList);
        return (
            <>
                <div id={'GalleryId:' + galleryData.GalleryId} className='gallery-container'>
                    <div className='gallery-toggle-container'>
                        <button className='gallery-toggle custom' onClick={this.toggleGallery}>
                            {oldGalleryTitle}
                            {/* , ID:{galleryData.GalleryId}, Image Count:({galleryData.ImageCount}) */}
                        </button>
                        <button className='image-count custom'>[{imageList.length}]</button>
                        <button className='action custom' onClick={this.toggleRemovePopup}>
                            <img src={removeIcon} alt='remove gallery' />
                        </button>
                        <button className='action custom' onClick={this.togglePopup}>
                            <img src={addIcon} alt='add gallery' />
                        </button>
                        <button className='action custom' onClick={this.toggleUpdatePopup}>
                            <img src={editIcon} alt='edit gallery' />
                        </button>
                    </div>
                    {imageList.map(image => (
                        <Image
                            hidden={isGalleryOpen}
                            key={'' + image.GalleryId + ':' + image.ImageId}
                            imageData={image}
                        />
                    ))}
                </div>
                <Popup
                    key='AddImage'
                    handleClose={this.togglePopup}
                    isPopupOpen={isPopupOpen}
                    content={
                        <>
                            <h3>Add Image:</h3>
                            <div className='input-group'>
                                <label htmlFor='AddImageTitle'>Title: </label>
                                <input
                                    maxLength='45'
                                    onChange={this.handleOnChange}
                                    name='AddImageTitle'
                                    required
                                />
                            </div>
                            <div className='input-group'>
                                <label htmlFor='URL'>URL: </label>
                                <input
                                    maxLength='2000'
                                    onChange={this.handleOnChange}
                                    name='URL'
                                    required
                                />
                            </div>
                            {/* Use () => because we want to run the function with that input, 
                    rather than call the function here */}
                            <p className='error-message left popup'>{AddImageMessage}</p>
                            <button
                                className='primary'
                                type='submit'
                                onClick={() => {
                                    this.handleAddImageSubmit(galleryData.GalleryId);
                                }}
                            >
                                Save
                            </button>
                            <br />
                        </>
                    }
                />
                <Popup
                    key='UpdateGallery'
                    handleClose={this.toggleUpdatePopup}
                    isPopupOpen={isUpdatePopupOpen}
                    content={
                        <>
                            <h3>Update Gallery:</h3>
                            <div className='input-group'>
                                <label htmlFor='UpdateGalleryTitle'>Title: </label>
                                <input
                                    maxLength='45'
                                    onChange={this.handleOnChange}
                                    name='UpdateGalleryTitle'
                                    defaultValue={galleryTitle}
                                    required
                                />
                            </div>
                            <p className='error-message left popup'>{UpdateGalleryMessage}</p>
                            <button
                                className='primary'
                                type='submit'
                                onClick={() => {
                                    this.handleUpdateGallerySubmit(galleryData.GalleryId);
                                }}
                            >
                                Save
                            </button>
                            <br />
                        </>
                    }
                />
                <Popup
                    key='RemoveGallery'
                    handleClose={this.toggleRemovePopup}
                    isPopupOpen={isRemovePopupOpen}
                    content={
                        <>
                            <h3>Remove Gallery:</h3>
                            <br />
                            <p className='left popup center'>
                                Are you sure you want to remove "{oldGalleryTitle}"?
                            </p>
                            <p className='error-message left popup'>{RemoveGalleryMessage}</p>
                            <div className='button-group'>
                                <button
                                    className='primary'
                                    type='submit'
                                    onClick={() => {
                                        this.handleRemoveGallerySubmit(galleryData.GalleryId);
                                    }}
                                >
                                    Remove
                                </button>
                                <button
                                    className='secondary light'
                                    type='submit'
                                    onClick={() => {
                                        this.toggleRemovePopup();
                                    }}
                                >
                                    Cancel
                                </button>
                            </div>
                        </>
                    }
                />
            </>
        );
    }
}

class GalleryPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            galleryList: [],
            // "GalleryId": <int>,
            // "ImageCount": <int>,
            // "Title": <string>
            AddGalleryMessage: '',
            isAddPopupOpen: false,
            AddGalleryTitle: '',
        };
    }

    // Load galleries on page load
    componentDidMount() {
        // Fetch gallery information
        let requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                sessionId: localStorage.getItem('sessionId'),
            },
        };

        fetch(settings.hostURL + 'GetGallery/', requestOptions)
            .then(res => res.json())
            .then(data => {
                // If success, load the galleryList
                if (data.Result === 'Success') {
                    this.setState({ galleryList: data.Message });
                } else {
                    this.setState({ galleryList: null });
                }
            })
            .catch(console.log);
    }

    handleAddGallerySubmit() {
        if (this.state.AddGalleryTitle.length === 0) {
            this.setState({
                AddGalleryMessage: 'The title cannot be empty',
            });
            return;
        }
        let requestOptions = {
            method: 'POST',
            headers: {
                sessionId: localStorage.getItem('sessionId'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Title: this.state.AddGalleryTitle,
            }),
        };

        fetch(settings.hostURL + 'AddGallery', requestOptions)
            .then(res => res.json())
            .then(data => {
                // console.log(data);
                if (data.Result === 'Success') {
                    this.setState({
                        galleryList: data.Message,
                        isAddPopupOpen: false,
                        AddGalleryMessage: '',
                    });
                    window.location.reload();
                } else {
                    this.setState({ AddGalleryMessage: 'Uanble to add gallery: ' + data.Result });
                }
            })
            .catch(console.log);
    }

    toggleAddGalleryPopup = () => {
        this.setState({
            isAddPopupOpen: !this.state.isAddPopupOpen,
            AddGalleryMessage: '',
            AddGalleryTitle: '',
        });
    };

    handleOnChange = e => {
        let Title;

        if (e.target.name === 'AddGalleryTitle') {
            Title = e.target.value;
            this.setState({ AddGalleryTitle: Title });
        }
    };

    toggleAllGalleries = () => {
        let galleryToggleButtons = document.getElementsByClassName('gallery-toggle');
        let closeGalleries = false;

        for (let i = 0; i < galleryToggleButtons.length; i++) {
            if (galleryToggleButtons[i].classList.contains('active')) {
                closeGalleries = true;
            }
        }

        for (let i = 0; i < galleryToggleButtons.length; i++) {
            let galleryButton = galleryToggleButtons[i];
            if (closeGalleries && galleryButton.classList.contains('active')) {
                galleryButton.click();
            }

            if (!closeGalleries && !galleryButton.classList.contains('active')) {
                galleryButton.click();
            }
        }
    };

    render() {
        // If there are any gallaries returned, add the gallery class
        const { galleryList, isAddPopupOpen, AddGalleryMessage } = this.state;
        if (galleryList) {
            return (
                <>
                    <div className='tools-container'>
                        <ImageSizeCheckbox />
                        <button
                            id='toggle-all-gallery'
                            className='secondary'
                            onClick={this.toggleAllGalleries}
                        >
                            Toggle All
                        </button>
                        <button
                            id='add-gallery'
                            className='primary'
                            onClick={this.toggleAddGalleryPopup}
                        >
                            Add Gallery
                        </button>
                    </div>
                    {galleryList.map(gallery => (
                        <Gallery key={gallery.GalleryId} galleryData={gallery} />
                    ))}
                    <Popup
                        handleClose={this.toggleAddGalleryPopup}
                        isPopupOpen={isAddPopupOpen}
                        content={
                            <>
                                <h3>Add Gallery:</h3>
                                <div className='input-group'>
                                    <label htmlFor='AddGalleryTitle'>Title: </label>
                                    <input
                                        maxLength='45'
                                        onChange={this.handleOnChange}
                                        name='AddGalleryTitle'
                                    />
                                </div>
                                <p className='error-message left popup'>{AddGalleryMessage}</p>
                                <button
                                    className='primary'
                                    type='submit'
                                    onClick={() => {
                                        this.handleAddGallerySubmit();
                                    }}
                                >
                                    Save
                                </button>
                            </>
                        }
                    />
                </>
            );
        } else {
            return (
                <>
                    <ImageSizeCheckbox />
                </>
            );
        }
    }
}

class ImageModal extends React.Component {
    constructor(props) {
        super(props);
        this.ImageId = -1;
    }

    changeImage = direction => event => {
        let currentImage;

        try {
            currentImage = document.getElementById('ImageId:' + event.target.value);
        } catch {
            return;
        }

        let nextImage = currentImage.nextElementSibling;
        let prevImage = currentImage.previousSibling;

        // We are at the end of the gallery
        if (!nextImage && direction === 1) {
            return;
        }
        if (!prevImage && direction === -1) {
            return;
        }
        if (!prevImage.getAttribute('value') && direction === -1) {
            return;
        }

        // Same logic as per the Image component, but using nextImage instead

        // Container for modal
        let modal = document.getElementById('selected-image-modal');

        // Modal img element
        let modalImg = document.getElementById('modal-image');

        // Container for image
        //let imageContainer = document.getElementById("ImageId:" + this.props.imageData.ImageId);
        let imageContainer = direction === 1 ? nextImage : prevImage;

        // The selected img element
        let image = imageContainer.childNodes[0];

        modal.style.display = 'block';
        modalImg.src = image.src;
        modal.childNodes[1].innerText = image.alt;

        // Update buttons

        // Prev
        if (direction === 1) {
            modal.childNodes[2].value = nextImage.getAttribute('value');
        }
        if (direction === -1) {
            modal.childNodes[2].value = prevImage.getAttribute('value');
        }

        // Next
        modal.childNodes[3].value = modal.childNodes[2].value;

        modal.classList.toggle('active');

        // Close button
        var closeButton = modal.childNodes[4];

        // When the user clicks on <span> (x), close the modal
        closeButton.onclick = function () {
            modal.style.display = 'none';
        };
    };

    render() {
        return (
            <div id='selected-image-modal' className='modal'>
                <img className='modal-content' id='modal-image' alt='selected' />
                <div id='caption'></div>
                <button
                    className='image-navigation image-left custom'
                    id='prevImage'
                    value=''
                    onClick={this.changeImage(-1)}
                >
                    {'<'}
                </button>
                <button
                    className='image-navigation image-right custom'
                    id='nextImage'
                    value=''
                    onClick={this.changeImage(1)}
                >
                    {'>'}
                </button>
                <span className='close'>&times;</span>
            </div>
        );
    }
}

export { GalleryPage, ImageModal };
