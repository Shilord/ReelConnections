# Reel Connections
[![Coverage Status](https://coveralls.io/repos/github/Shilord/ReelConnections/badge.svg?branch=redirect-and-readme-updates)](https://coveralls.io/github/Shilord/ReelConnections?branch=redirect-and-readme-updates)
![Workflow Status](https://github.com/Shilord/ReelConnections/actions/workflows/build_test.yml/badge.svg)

[Play the game here](https://reelconnections.streamlit.app/)

## Developer Note
This repository is an extended, solo continuation of a V1 project originally developed over a five-week period spanning February and March of 2026. While the foundation was built collaboratively for a school assignment (Data515 at the University of Washington), all commits, architecture changes, and feature expansions since are my own independent work.

## Game Info
### What is Reel Connections: 
This project aims to create a web app that allows users to test their movie and actor knowledge in the form of a game inspired by popular parlor game [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon). In this game, users are given a random starting actor and random target actor. They then connect the starting actor to another actor through a film they both appear in, and repeat until they reach the target actor. The goal of the game is to reach the target actor in as few movie + actor combinations as possible. An alternate, more challenging game mode is featured as well, in which players once again choose movie + actor combinations to reach the target actor, but score higher the lower the total box office sales (adjusted for inflation) of their chosen movies is, incentivizing creative picks of less well-known movies over simply the shortest path to the target actor. For each game mode, three difficulty levels are offered (easier difficulties restrict the game to more popular actors).

### How it Works:
On the back-end of this game, data has been retrieved, processed, and formatted to create the necessary web of connections between actors and movies (please see **Data Sources**). This information is stored into efficient nested dictionaries, and search algorithms based on BFS and Dijkstra's algorithm are used to calculate the optimal solution between two random start and end actors. Scores are given to players based on how far their selections deviate from the optimal.

### Data Sources:
Data is collected from the following sources: 
- ~~[IMDb's Non-Commercial Datasets for movie and actor lists](https://developer.imdb.com/non-commercial-datasets/)~~(This was true in previous game versions, but is no longer in use.)
- [TMDb API for both actor and movie information](https://developer.themoviedb.org/docs/getting-started)
- [Inflation Data provided by the US Bureau of Labor Statistics](https://data.bls.gov/timeseries/CUUR0000SA0L1E?output_view=pct_12mths)

## Background
### Current Project Members: 
[Henry Shi](https://github.com/Shilord)

### Original Project Members: 
[Henry Shi](https://github.com/Shilord), [Owen Guo](https://github.com/haiguo123), [Zach Lubarsky](https://github.com/zlubars), [Daniel Yan](https://github.com/danielyan21)

### Original Project Repo:
[https://github.com/Shilord/Data515_MediaAnalysis_FinalProj](https://github.com/Shilord/Data515_MediaAnalysis_FinalProj) 

### Purpose:
My reasons for expanding on this game solo remains in line with the original purpose of this project when it was still a school assignment: "Through the development of this game/web app, we seek to enforce strong data science and software engineering practices including: 1) data acquisition, cleaning, merging, and analysis, 2) unit testing and modular programming, 3) writing code and algorithms for game/app logic, 4) following good development conventions with version control, CI/CD, linting, etc., and 5) designing a smooth UI experience with all of the data science and code abstracted away. We hope to provide an engaging and seamless game for users to enjoy."

## Repo Structure
**data/** - Retrieval/processing scripts and stored data.

**demo/** - A demo recording demonstrating the use/play of this game. This recording is outdated and based on the V1 version (the final version for this project as a school assignemnt).

**docs/** - Includes documentation created primarily during the ideation phase as well as the final presentation slides for when this was still a school assignment.

**streamlit/** - The code for the app, including both the UI (created and deployed via Streamlit) and back-end logic. 

---

## Setting Up the Virtual Environment

This project uses **Conda** to manage dependencies and ensure a consistent environment across all collaborators.

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download) installed on your machine.

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Shilord/ReelConnections.git
cd ReelConnections
```

**2. Create the conda environment**

This installs Python 3.13 and all required dependencies defined in `environment.yml`:
```bash
conda env create -f environment.yml
```

**3. Activate the environment**
```bash
conda activate reel-connections
```

You should see `(reel-connections)` at the start of your terminal prompt confirming the environment is active.

**4. Run the app**
```bash
streamlit run streamlit/app.py
```

### Updating the Environment

If dependencies change (e.g. after pulling new changes), update your local environment:
```bash
conda env update -f environment.yml --prune
```

The `--prune` flag removes any packages that are no longer needed.

### Deactivating the Environment

When you're done working:
```bash
conda deactivate
```

### Removing the Environment

If you need to start fresh:
```bash
conda remove --name reel-connections --all
```

---

## Running Tests

From the repo root with the environment active:
```bash
cd streamlit
coverage run -m unittest discover -s tests -t tests
coverage report
```

## Running the Linter

```bash
pylint --recursive=y --source-roots=streamlit streamlit/core/
pylint --recursive=y --source-roots=streamlit streamlit/tests/
```
