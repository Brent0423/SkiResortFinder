# Ski Resort Finder

Welcome to Ski Resort Finder, your ultimate Flask-based web application for discovering and comparing ski resorts based on up-to-date snow conditions. This tool is perfect for planning your next ski trip or just exploring options for future snowy adventures.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Features

Real-time Updates: Get the latest information on snow conditions including snowfall and depth.
Resort Search: Find specific ski resorts or discover new destinations.
Resort Rankings: See resorts ranked by snow conditions to plan your perfect getaway.
Intuitive Interface: Navigate the app with ease thanks to a user-friendly design.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker
- Python (3.6 or higher)
- Flask
- Requests
- Dotenv

### Installation

To set up Ski Resort Finder on your local machine:

1. Clone the repository: git clone https://github.com/Brent0423/SkiResortFinder.git
2. Navigate to the project directory: cd SkiResortFinder
3. Build the Docker image: docker build -t skiresortfinder .
4. Run the Docker container: docker-compose up
5. Access the app at http://localhost:5000.

## How It Works

The Ski Resort Finder operates through a series of programmed functionalities designed to fetch, process, and display the most current and comprehensive ski resort data. Here's a breakdown of the key processes:

### Data Fetching and Processing

#### Parsing Snow Depth Measurements

- Formula: If measurement is in cm, convert to inches using the conversion rate (1cm = 0.393701 inches). If the measurement is in inches, use it directly.
- Purpose: Ensures uniformity in snow depth measurements across the dataset, crucial for accurate comparisons and analyses.

#### Fetching Single Resort Data

- Operations:
  - Encode resort name for URL compatibility.
  - Perform a GET request to retrieve data.
  - Implement error handling to manage request failures.
- Purpose: Retrieves detailed information for each resort, managing API nuances such as request delays and errors.

#### Fetching Resort Data Sequentially

- Formula: Sequentially call fetch_single_resort_data(resort) for each resort in a given list, aggregating the data.
- Purpose: Collects comprehensive data for multiple resorts, ensuring the application respects API rate limits and avoids data source overload.

### Resort Ranking and Display

#### Processing Resort Data

- Formula: Extract and convert snow depth data, organizing it along with essential details like the resort's region.
- Purpose: Transforms raw data into a structured and usable format for analysis and comparison.

#### Sorting Resorts Based on Normalized Snow Condition Scores

- Formula: Calculate a normalized score for each resort by dividing its score by the maximum score and then multiplying by 100.
- Purpose: Ranks resorts based on snow conditions, providing a quantified basis for comparison.

### Data Management

#### Saving Resort Data to a JSON File

- Operation: Use json.dump to write processed data to a file with proper indentation.
- Purpose: Securely stores and makes processed data easily accessible and sharable.

### Execution and Modularity

#### Main Execution Block

- Flow: If executed directly, the script fetches, processes, sorts, and saves resort data.
- Purpose: Enhances script reusability and modularity, allowing for standalone operation or integration into larger systems.

## Project Structure

The application is organized as follows:

- app.py: Entry point for the Flask application.
- search.py: Handles the functionality for searching ski resorts.
- main.py: Contains functions for fetching and processing resort data.
- requirements.txt: Lists the Python dependencies.
- Docker files: Dockerfile and docker-compose.yml for container setup.
- Documentation: readme.md.

## Technologies Used

- Flask: Serves as the backend framework for creating the web application.
- Docker: Utilized for containerizing the application, facilitating easy deployment and consistency across environments.
