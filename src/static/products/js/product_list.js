function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


const csrftoken = getCookie('csrftoken');




document.querySelectorAll('#wishlist').forEach(function (element) {
    element.addEventListener('click', function (event) {
      event.preventDefault();
      const url = this.getAttribute('name');
      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.querySelector('i').classList.toggle('bi-heart');
          this.querySelector('i').classList.toggle('bi-heart-fill');
          this.querySelector('i').classList.toggle('text-danger');
        } else {
          alert(data.error);
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });