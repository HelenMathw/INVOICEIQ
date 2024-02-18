// Interactive elements
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        navLinks.forEach(link => {
          link.classList.remove('active');
        });
        this.classList.add('active');
      });
    });
    
    const uploadForm = document.getElementById('upload-form');
    
    uploadForm.addEventListener('submit', function(e) {
      e.preventDefault();
      // Your upload functionality here
      alert('Upload functionality will be implemented here.');
    });
  });
  