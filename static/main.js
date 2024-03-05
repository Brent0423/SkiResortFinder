document.addEventListener('DOMContentLoaded', function() {
    // Fetch top resorts data immediately on page load
    fetchResortData('/api/resorts', true); // Endpoint assumed to return all resorts

    // Event listener for the search button
    document.getElementById('resortSearchButton').addEventListener('click', function() {
        var resortName = document.getElementById('resortSearchBox').value;
        if (resortName) {
            // Format resort name for URL
            var formattedResortName = resortName.replace(/ /g, '%20');
            // Fetch resort data based on search input
            fetch(`/api/search?resort=${formattedResortName}`)
                .then(response => response.json())
                .then(data => {
                    // Display individual resort data
                    individualResortData(data);
                    // Open modal to show the data
                    openModal('searchModal');
                })
                .catch(error => console.error('Error fetching data:', error));
        }
    });

    // Event listener for pressing Enter in the search input field
    document.getElementById('resortSearchBox').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            // Trigger click event on the search button
            document.getElementById('resortSearchButton').click();
        }
    });

    // Event listener for the "Show All Resorts" button
    document.getElementById('thebutton').addEventListener('click', function() {
        // Fetch and display all resorts data
        fetchResortData('/api/resorts');
    });

    // Function to fetch and display resort data
    function fetchResortData(url, updateTopResortsImmediately = false) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Log the retrieved data
                console.log("Fetched data:", data);
                // Display fetched data in modal
                displayResortData(data);

                if (updateTopResortsImmediately) {
                    // Immediately update the top resorts list with all resorts
                    updateTopResortsList(data);
                } else {
                    // Open modal to show all resorts
                    openModal('showAllModal');
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to display fetched resort data inside the modal
    function displayResortData(data) {
        console.log("Inside displayResortData function");
        console.log("Resort data:", data);

        // Log the structure of the first item in the data array
        if (data.length > 0) {
            console.log("First item structure:", Object.keys(data[0]));
        }

        var modalContent = document.getElementById('showAllModalContent');
        if (!modalContent) {
            console.error("Modal content element not found");
            return;
        }
        modalContent.innerHTML = ''; // Clear previous content

        // Adjust column headers to include "REGION"
        document.querySelector("#showAllTable th:nth-child(1)").textContent = "RANK";
        document.querySelector("#showAllTable th:nth-child(2)").textContent = "RESORT";
        document.querySelector("#showAllTable th:nth-child(3)").textContent = "REGION"; // Ensure this is added if missing
        document.querySelector("#showAllTable th:nth-child(4)").textContent = "SCORE"; // Shift SCORE to fourth column

        // Check if data is an array
        if (!Array.isArray(data)) {
            console.error("Data is not an array");
            return;
        }

        // Populate table rows with resort data, including the region
        data.forEach((resort, index) => {
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${resort.name}</td>
                <td>${resort.region || 'N/A'}</td> <!-- Include region here -->
                <td>${resort.score}</td>
            `;
            modalContent.appendChild(row);
        });
    }

    // Function to update top resorts list
    function updateTopResortsList(resorts) {
        var resortList = document.querySelectorAll('.resort-list .resort');
        // Clear existing list content before updating
        resortList.forEach((item, index) => {
            if (resorts[index]) {
                item.innerHTML = `${resorts[index].name || 'N/A'}`;
            } else {
                item.innerHTML = ''; // Clear any resorts not in the top 5
            }
        });
    }

    // Function to display individual resort data inside the modal
    function individualResortData(data) {
        var modalContent = document.getElementById('searchModalContent');
        modalContent.innerHTML = ''; // Clear previous content

        // Adjust column headers
        document.querySelector("#searchTable th:nth-child(1)").textContent = "Resort";
        document.querySelector("#searchTable th:nth-child(2)").textContent = "Region";
        document.querySelector("#searchTable th:nth-child(3)").textContent = "Bottom Snow Depth";
        document.querySelector("#searchTable th:nth-child(4)").textContent = "Top Snow Depth";
        document.querySelector("#searchTable th:nth-child(5)").textContent = "Recent Snowfall Amount";
        document.querySelector("#searchTable th:nth-child(6)").textContent = "Last Snowfall Date";

        // Populate table row with individual resort data
        var row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.basicInfo.name}</td>
            <td>${data.region || 'N/A'}</td> // Fix for missing or incorrect region
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
