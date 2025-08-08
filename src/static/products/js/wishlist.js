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
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({})
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          location.reload();
        } else if (data.error) {
          alert(data.error);
        }
      });
    });
  });

  document.querySelectorAll('#add-to-cart').forEach(function (element) {
    element.addEventListener('click', function (event) {
      event.preventDefault();
      const url = this.getAttribute('name');
      let product_id = this.getAttribute('data-product-id');
      let quantityElem = document.getElementById('quantity');
      let quantity = (quantityElem && quantityElem.value) ? quantityElem.value : 1;
      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: product_id,
          quantity: quantity
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
            // Show a successful notification
            let notification = document.createElement('div');
            notification.textContent = 'Product added to cart!';
            notification.style.position = 'fixed';
            notification.style.top = '20px';
            notification.style.right = '20px';
            notification.style.backgroundColor = '#28a745';
            notification.style.color = 'white';
            notification.style.padding = '12px 24px';
            notification.style.borderRadius = '8px';
            notification.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
            notification.style.zIndex = 9999;
            notification.style.fontWeight = 'bold';
            document.body.appendChild(notification);
            setTimeout(function() {
              notification.remove();
            }, 2000);
        } else {
          this.textContent = 'Add to Cart';
          this.classList.remove('disabled');
          this.classList.add('add-to-cart');
          this.classList.remove('btn-success');
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });
