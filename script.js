document.addEventListener("DOMContentLoaded", () => {
    const slideshowContainer = document.getElementById("slideshow-container");
    const dotContainer = document.getElementById("dot-container");
    const imageFolder = "camera-1";  // Folder where images are stored
  
    // Function to fetch image names dynamically
    async function fetchImageNames() {
      const response = await fetch(imageFolder);
      const text = await response.text();
      const parser = new DOMParser();
      const htmlDoc = parser.parseFromString(text, 'text/html');
      const imageElements = htmlDoc.querySelectorAll('a');
      
      let images = [];
      imageElements.forEach(imageElement => {
        const href = imageElement.getAttribute('href');
        if (href.match(/\.(jpg|jpeg|png|gif)$/)) {
          images.push(href);
        }
      });
      
      return images;
    }
  
    // Function to create the slideshow
    async function createSlideshow() {
      const images = await fetchImageNames();
      let slideIndex = 0;
      
      images.forEach((image, index) => {
        const slide = document.createElement('div');
        slide.classList.add('mySlides');
        if (index === 0) slide.classList.add('active');
  
        const img = document.createElement('img');
        img.src = `${imageFolder}/${image}`;
        img.style.width = '100%';
        slide.appendChild(img);
  
        slideshowContainer.appendChild(slide);
  
        const dot = document.createElement('span');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dotContainer.appendChild(dot);
      });
  
      function showSlides() {
        const slides = document.querySelectorAll('.mySlides');
        const dots = document.querySelectorAll('.dot');
        
        slides.forEach((slide, i) => {
          slide.style.display = 'none';
          dots[i].classList.remove('active');
        });
  
        slideIndex++;
        if (slideIndex > slides.length) slideIndex = 1;
  
        slides[slideIndex - 1].style.display = 'block';
        dots[slideIndex - 1].classList.add('active');
  
        setTimeout(showSlides, 1000); // Change image every 1 second
      }
  
      showSlides();
    }
  
    createSlideshow();
  });
  
  