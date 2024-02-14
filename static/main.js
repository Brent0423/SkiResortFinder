document.addEventListener('DOMContentLoaded', function() {
    // Event listener for the search button
    document.getElementById('resortSearchButton').addEventListener('click', function() {
        var resortName = document.getElementById('resortSearchBox').value;
        if (resortName) {
            var formattedResortName = resortName.replace(/ /g, '%20');
            fetch(`/api/search?resort=${formattedResortName}`)
                .then(response => response.json())
                .then(data => {
                    // Handle the fetched resort data
                    individualResortData(data);
                    // Open the modal to show the data
                    openModal('searchModal');
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
                openModal('showAllModal'); // Open the modal to show the data
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to display fetched resort data inside the modal
    function displayResortData(data) {
        var modalContent = document.getElementById('showAllModalContent');
        modalContent.innerHTML = ''; // Clear previous content

        // Adjust column headers
        document.querySelector("#showAllTable th:nth-child(1)").textContent = "RANK";
        document.querySelector("#showAllTable th:nth-child(2)").textContent = "RESORT";
        document.querySelector("#showAllTable th:nth-child(3)").textContent = "SCORE";

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

    // Function to display individual resort data inside the modal
    function individualResortData(data) {
        var modalContent = document.getElementById('searchModalContent');
        modalContent.innerHTML = ''; // Clear previous content

        // Adjust column headers
        document.querySelector("#searchTable th:nth-child(1)").textContent = "Name";
        document.querySelector("#searchTable th:nth-child(2)").textContent = "Region";
        document.querySelector("#searchTable th:nth-child(3)").textContent = "Bottom Snow Depth";
        document.querySelector("#searchTable th:nth-child(4)").textContent = "Top Snow Depth";
        document.querySelector("#searchTable th:nth-child(5)").textContent = "Recent Snowfall Amount";
        document.querySelector("#searchTable th:nth-child(6)").textContent = "Last Snowfall Date";

        // Create row for individual resort
        var row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.basicInfo.name}</td>
            <td>${data.basicInfo.region}</td>
            <td>${data.botSnowDepth}</td>
            <td>${data.topSnowDepth}</td>
            <td>${data.freshSnowfall}</td>
            <td>${data.lastSnowfallDate}</td>
        `;
        modalContent.appendChild(row);
    }

    // Function to open the modal
    function openModal(modalId) {
        var modal = document.getElementById(modalId);
        modal.style.display = "block";
    }

    // Event listener for the close button of the modal
    document.querySelectorAll('.close').forEach(function(closeButton) {
        closeButton.addEventListener('click', function() {
            closeModal(this.parentElement.parentElement.id);
        });
    });

    // Function to close the modal
    function closeModal(modalId) {
        var modal = document.getElementById(modalId);
        modal.style.display = "none";
    }

    // Optional: Close the modal when clicking outside of it
    window.addEventListener('click', function(event) {
        ['searchModal', 'showAllModal'].forEach(function(modalId) {
            var modal = document.getElementById(modalId);
            if (event.target == modal) {
                closeModal(modalId);
            }
        });
    });
});
