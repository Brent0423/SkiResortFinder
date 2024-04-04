# USA Ski Resort Ranker

USA Ski Resort Ranker is a Flask-based web application designed to help skiers and snowboarders discover the best ski resorts in the United States based on up-to-date snow conditions. This tool is perfect for planning your next ski trip or exploring potential destinations for future snowy adventures.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Data Fetching and Processing](#data-fetching-and-processing)
- [Resort Ranking and Display](#resort-ranking-and-display)
- [Data Management](#data-management)
- [Execution and Modularity](#execution-and-modularity)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Resort Rankings Numerical Value Calculation](#resort-rankings-numerical-value-calculation)

## Features

- **Real-time Snow Updates:** Get the latest information on snow conditions, including snowfall and depth, ensuring you have access to the most current data when planning your trip.
- **Resort Search:** Easily find specific ski resorts or discover new destinations with the intuitive search functionality.
- **Resort Rankings:** View resorts ranked by snow conditions, allowing you to quickly identify the top locations with the best snow quality for your desired timeframe.
- **User-Friendly Interface:** Navigate the application seamlessly with a clean and intuitive design, enhancing the overall user experience.

## Getting Started

### Prerequisites

Before setting up the USA Ski Resort Ranker, ensure you have the following installed on your system:

- Docker
- Python (version 3.6 or higher)
- Flask
- Requests
- Dotenv

### Installation

Follow these steps to set up the USA Ski Resort Ranker on your local machine:

1. Clone the repository: `git clone https://github.com/Brent0423/SkiResortFinder.git`
2. Navigate to the project directory: `cd SkiResortFinder`
3. Build the Docker image: `docker build -t skiresortfinder .`
4. Run the Docker container: `docker-compose up`
5. Access the app by visiting [http://localhost:8081](http://localhost:8081) in your web browser.

## How It Works

### Data Fetching and Processing

- **Parsing Snow Depth Measurements:** The application ensures uniformity in snow depth measurements across the dataset by converting centimeter measurements to inches (1 cm = 0.393701 inches) and using inch measurements directly. This step is crucial for accurate comparisons and analyses.
- **Fetching Single Resort Data:** The application encodes resort names for URL compatibility, performs GET requests to retrieve data, and implements error handling to manage request failures. This process retrieves detailed information for each resort, managing API nuances such as request delays and errors.
- **Fetching Resort Data Sequentially:** The application sequentially calls the `fetch_single_resort_data` function for each resort in a given list, aggregating the data. This approach ensures that the application respects API rate limits and avoids overloading the data source.

### Resort Ranking and Display

- **Processing Resort Data:** The application extracts and converts snow depth data, organizing it along with essential details like the resort's region. This step transforms raw data into a structured and usable format for analysis and comparison.
- **Sorting Resorts Based on Normalized Snow Condition Scores:** The application calculates a normalized score for each resort by dividing its score by the maximum score and then multiplying by 100. This process ranks resorts based on snow conditions, providing a quantified basis for comparison.

### Data Management

- **Saving Resort Data to a JSON File:** The application uses the `json.dump` function to write processed data to a file with proper indentation. This operation securely stores and makes processed data easily accessible and sharable.

### Execution and Modularity

- **Main Execution Block:** When executed directly, the script fetches, processes, sorts, and saves resort data. This approach enhances script reusability and modularity, allowing for standalone operation or integration into larger systems.

## Project Structure

The application is organized as follows:

- `app.py`: Entry point for the Flask application.
- `search.py`: Handles the functionality for searching ski resorts.
- `main.py`: Contains functions for fetching and processing resort data.
- `requirements.txt`: Lists the Python dependencies.
- Docker files: Includes `Dockerfile` and `docker-compose.yml` for container setup.
- Documentation: `readme.md` provides detailed documentation for the project.

## Technologies Used

- **Flask:** Serves as the backend framework for creating the web application.
- **Docker:** Utilized for containerizing the application, facilitating easy deployment and consistency across environments.

## Resort Rankings Numerical Value Calculation

The numerical value for resort rankings is calculated through the following detailed steps:

1. **Summation of Scores:** Each resort's scores for `topSnowDepth`, `botSnowDepth`, and `freshSnowfall` are summed up. These scores are initially in percentage format, so the '%' is removed, and the values are converted to floats before summation.
2. **Normalization:** The method identifies the maximum total score among all resorts. Each resort's total score is then divided by this maximum score, normalizing the scores on a scale where the highest score equals 100. This step ensures that the scores are relative to the best-performing resort.
3. **Percentage Conversion:** The normalized scores are multiplied by 100 to convert them into a percentage format. This conversion facilitates easier interpretation of the scores, indicating each resort's performance relative to the top-performing resort on a 0 to 100 scale.
4. **Sorting:** Resorts are sorted in descending order based on their normalized scores. This ranking reflects the relative performance of the resorts, with higher scores indicating superior snow conditions.
