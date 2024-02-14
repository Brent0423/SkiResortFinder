document.addEventListener('DOMContentLoaded', function() {
    // Event listener for the search button
    document.getElementById('resortSearchButton').addEventListener('click', function() {
        var resortName = document.getElementById('resortSearchBox').value;
        if (resortName) {
            // Replace spaces with '%20' to ensure the URL is encoded correctly
            var formattedResortName = resortName.replace(/ /g, '%20');
            // Fetch resort data using the API (assuming you have an endpoint set up)
            fetch(`/api/search?resort=${formattedResortName}`)
                .then(response => response.json())
                .then(data => {
                    // Handle the fetched resort data
                    displayResortData(data);
                    // Open the modal to show the data
                    openModal();
                })
                .catch(error => console.error('Error fetching data:', error));
        }
    });

    // Event listener for the "Show All Resorts" button
    document.getElementById('thebutton').addEventListener('click', function() {
        fetchResortData('/api/resorts'); // Assuming '/api/resorts' returns all resorts
    });

    // Function to fetch and display resort data
    function fetchResortData(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                displayResortData(data); // Display fetched data
                openModal(); // Open the modal to show the data
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to display fetched resort data inside the modal
    function displayResortData(data) {
        var modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = ''; // Clear previous content
        data.forEach((resort, index) => {
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${resort.name}</td>
                <td>${resort.score}</td>
            `;
            modalContent.appendChild(row);
        });
    }

    // Function to open the modal
    function openModal() {
        var modal = document.getElementById('myModal');
        modal.style.display = "block";
    }

    // Event listener for the close button of the modal
    document.querySelector('#myModal .close').addEventListener('click', function() {
        closeModal();
    });

    // Function to close the modal
    function closeModal() {
        var modal = document.getElementById('myModal');
        modal.style.display = "none";
    }

    // Optional: Close the modal when clicking outside of it
    window.addEventListener('click', function(event) {
        var modal = document.getElementById('myModal');
        if (event.target == modal) {
            closeModal();
        }
    });
});
