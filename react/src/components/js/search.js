function imageSearch(input) {
    //let input = document.getElementById("top-search");
    let filter = input.trim();

    // Get all images
    let image = document.getElementsByClassName('gallery-image');
    for (let i = 0; i < image.length; i++) {
        let imageTitle = image[i].nextElementSibling.childNodes[1];
        let textValue = imageTitle.textContent || imageTitle.innerText;
        if (textValue.toUpperCase().indexOf(filter) > -1) {
            image[i].parentElement.style.display = 'block';
        } else {
            image[i].parentElement.style.display = 'none';
        }
    }
}

function gallerySearch(input) {
    let filter = input.trim();
    let gallery = document.getElementsByClassName('gallery-container');
    for (let i = 0; i < gallery.length; i++) {
        console.log(i);
        let galleryName = gallery[i].childNodes[0].childNodes[0].innerText;
        console.log(galleryName);
        if (galleryName.toUpperCase().indexOf(filter) > -1) {
            gallery[i].style.display = 'block';
        } else {
            gallery[i].style.display = 'none';
        }
    }
}

export function pageSearch(event) {
    let input = event.target.value.toUpperCase();

    // Keep search box open
    if (input.length > 0) {
        event.target.classList.add('complete');
    } else {
        event.target.classList.remove('complete');
    }

    try {
        input = document.getElementById('top-search').value.toUpperCase();
    } catch (error) {
        console.log(error);
    }

    if (input.match(/IMAGE:/g)) {
        gallerySearch('');
        imageSearch(input.substring(6, input.length));
    } else if (input.match(/GALLERY:/g)) {
        imageSearch('');
        gallerySearch(input.substring(8, input.length));
    } else {
        gallerySearch('');
        imageSearch(input);
    }
}
