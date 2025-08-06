document.addEventListener('DOMContentLoaded', setupProfilePicPreview);
// Attach event listeners to all remove buttons after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-outline-danger').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const addressId = this.closest('.card').querySelector('#address-id').textContent.trim();
            deleteAddress(addressId, this);
        });
    });
});
document.getElementById('change-user-type-btn').onclick = changeUserType;
document.addEventListener('DOMContentLoaded', function() {
    // Get the tab buttons
    const profileTabBtn = document.getElementById('v-pills-profile-tab');
    const addressesTabBtn = document.getElementById('v-pills-addresses-tab');

    // Get the tab panes
    const profileTabPane = document.getElementById('v-pills-profile');
    const addressesTabPane = document.getElementById('v-pills-addresses');

    // Helper to switch tabs
    function activateTab(tabBtn, tabPane) {
        // Remove 'active' from all tab buttons
        profileTabBtn.classList.remove('active');
        addressesTabBtn.classList.remove('active');

        // Remove 'show active' from all tab panes
        profileTabPane.classList.remove('show', 'active');
        addressesTabPane.classList.remove('show', 'active');

        // Add 'active' to clicked tab button
        tabBtn.classList.add('active');
        // Add 'show active' to corresponding tab pane
        tabPane.classList.add('show', 'active');
    }

    // Event listeners
    profileTabBtn.addEventListener('click', function(e) {
        e.preventDefault();
        activateTab(profileTabBtn, profileTabPane);
    });

    addressesTabBtn.addEventListener('click', function(e) {
        e.preventDefault();
        activateTab(addressesTabBtn, addressesTabPane);
    });
});

function setupProfilePicPreview() {
        document.getElementById('profile-pic-preview').onclick = function() {
        document.getElementById('profile_pic').click();
    };
        document.getElementById('profile_pic').onchange = function(event) {
        const [file] = event.target.files;
        if (file) {
            document.getElementById('profile-pic-preview').src = URL.createObjectURL(file);
}};}

function deleteAddress(addressId, btn) {
    console.log(addressId)
    if (!confirm('Are you sure you want to remove this address?')) return;
    fetch(`/user/delete_address/${addressId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the address card from the DOM
            const card = btn.closest('.col-md-6');
            if (card) card.remove();
        } else {
            alert(data.error || 'Failed to delete address.');
        }
    })
    .catch(() => {
        alert('An error occurred. Please try again.');
    });
}

function changeUserType(event) {
    event.preventDefault();
    const selectedRole = document.getElementById('user_role').options[document.getElementById('user_role').selectedIndex].value;
    console.log('Selected Role:', selectedRole);
    fetch('/user/role_change/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ role: selectedRole })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        if (data.success) {
            alert('Role change request submitted successfully.');
        } else {
            alert(data.error || 'Failed to submit role change request.');
        }
    })
    .catch(() => {
        alert('An error occurred. Please try again.');
    });
}
