# SkyBlock Stats

A Python application for retrieving and processing player statistics from **Hypixel SkyBlock**, using the Mojang and Hypixel APIs.

**Project Status:** Work in Progress — Backend Development

## Project Overview

SkyBlock Stats is a personal project I'm developing to improve my Python programming skills and gain practical experience working with APIs, data processing and application development.

The main goal is to build a reliable Python backend capable of retrieving and processing player data from Hypixel SkyBlock. Once the backend is sufficiently developed and tested, I plan to create a graphical user interface (GUI) to make the application easier to use.

Currently, the application runs through a command-line interface while I develop and test the backend functionality.

## Current Features

The project currently includes code for:

- **Player Lookup:** Retrieve a Minecraft player's UUID using their username through the Mojang API.
- **Profile Retrieval:** Fetch Hypixel SkyBlock profile data and identify the selected profile.
- **General Statistics:** Display SkyBlock level, purse balance, bank balance and collected Fairy Souls.
- **Skill Progression:** Calculate skill levels, experience towards the next level and overflow experience.
- **Armour and Equipment:** Decode inventory data to retrieve equipped items and their rarities.
- **Pet Information:** Identify and display the player's active pet and its rarity.
- **Data Formatting:** Format large numbers and remove Minecraft colour codes from item names.
- **Basic Error Handling:** Handle certain unsuccessful API responses.

Some functionality is still being tested and may not work for every player profile.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| HTTPX | Making HTTP requests to external APIs |
| Mojang API | Converting Minecraft usernames to UUIDs |
| Hypixel API | Retrieving SkyBlock player statistics |
| JSON | Processing API responses |
| NBTLib | Decoding Minecraft inventory data |
| Git & GitHub | Version control and project management |

## Installation and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/amartyakundu/skyblock-stats.git
cd skyblock-stats
```

### 2. Install Dependencies

Install the required Python libraries:

```bash
pip install httpx nbtlib
```

### 3. Configure the API Key

The application requires a Hypixel API key to access player statistics.

Create a file named `config.py` in the project directory and add:

```python
API_KEY = "YOUR_HYPIXEL_API_KEY"
```

**Important:** Keep your API key private. Ensure `config.py` is included in `.gitignore` and never commit your actual API key to the repository.

### 4. Run the Application

```bash
python Main.py
```

Enter a Minecraft username when prompted. The application will attempt to retrieve and display that player's SkyBlock statistics.

**Note:** As the project is still under development, some profiles or missing API data may cause errors.

## Project Structure

```text
skyblock-stats/
├── Main.py
├── formatting.py
├── inventory.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Main.py** — Handles player lookup, API requests, profile retrieval and command-line output.

**formatting.py** — Contains reusable functions for number formatting, skill calculations, colour-code removal and item rarity identification.

**inventory.py** — Handles decoding compressed and encoded Minecraft inventory data.

**requirements.txt** — Contains project dependencies.

## Development Roadmap

### Phase 1 — Backend Development (In Progress)

- [x] Implement Minecraft player lookup using the Mojang API.
- [x] Retrieve player profiles using the Hypixel API.
- [x] Identify the selected SkyBlock profile.
- [x] Retrieve and display general player statistics.
- [x] Implement skill level and experience progression calculations.
- [x] Decode armour and equipment inventory data.
- [x] Retrieve active pet information.
- [x] Create reusable formatting and inventory-processing functions.
- [ ] Improve error handling for missing or unexpected API data.
- [ ] Refactor the code into a more modular backend architecture.
- [ ] Expand the available player statistics.
- [ ] Test functionality across different player profiles.

### Phase 2 — GUI Development (Planned)

- [ ] Research and select a suitable GUI framework.
- [ ] Design an interface for searching Minecraft players.
- [ ] Create organised displays for player statistics.
- [ ] Integrate the GUI with the Python backend.
- [ ] Improve navigation and overall usability.

### Phase 3 — Testing and Improvements (Planned)

- [ ] Optimise API requests and data processing.
- [ ] Improve application performance and reliability.
- [ ] Introduce clearer error messages.
- [ ] Test the complete application.
- [ ] Package the application for easier installation and use.

## What I'm Learning

Through this project, I'm developing practical experience with:

- Writing and organising Python code.
- Making HTTP requests and working with REST APIs.
- Processing nested JSON responses.
- Working with encoded and compressed data.
- Creating reusable functions and separating code into modules.
- Debugging errors and handling unexpected data.
- Using Git and GitHub to manage a programming project.
- Planning application architecture for future GUI integration.

The project is also helping me understand how different parts of an application work together, particularly the separation between backend data processing and the user interface.

## Disclaimer

SkyBlock Stats is an independent personal project and is not affiliated with Hypixel, Mojang or Microsoft.

All player statistics are obtained through their respective APIs, and data availability depends on those services.
