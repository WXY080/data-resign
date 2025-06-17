let images = [];
let currentIndex = 0;

async function loadImages() {
    try {
        const response = await fetch('/api/images');
        const data = await response.json();
        images = data.images;
        document.getElementById('image-count').textContent = images.length;
        showNextImage();
    } catch (error) {
        showMessage('加载图片时出错', true);
    }
}

function showNextImage() {
    if (currentIndex >= images.length) {
        document.getElementById('current-image').style.display = 'none';
        document.getElementById('image-info').textContent = 'No more images to rate';
        document.getElementById('good-btn').disabled = true;
        document.getElementById('bad-btn').disabled = true;
        return;
    }
    
    const imageUrl = `/images/${images[currentIndex]}`;
    document.getElementById('current-image').src = imageUrl;
    document.getElementById('image-count').textContent = images.length - currentIndex;
}

async function rateImage(rating) {
    const image = images[currentIndex];
    try {
        const response = await fetch('/api/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image, rating }),
        });
        
        const result = await response.json();
        if (response.ok) {
            currentIndex++;
            showNextImage();
            showMessage('图片评价成功');
        } else {
            showMessage(result.error, true);
        }
    } catch (error) {
        showMessage('图片评价出错', true);
    }
}

function showMessage(message, isError = false) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.style.color = isError ? '#f44336' : '#4CAF50';
    setTimeout(() => {
        messageEl.textContent = '';
    }, 3000);
}

document.getElementById('good-btn').addEventListener('click', () => rateImage('good'));
document.getElementById('bad-btn').addEventListener('click', () => rateImage('bad'));

document.addEventListener('DOMContentLoaded', loadImages);