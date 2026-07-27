# Functional Specifications
## Background
This project aims to create a web app that allows users to test their movie and actor knowledge in the form of a game inspired by popular parlor game [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon). In this game, users will be given a random starting actor and random target actor. They then connect the starting actor to another actor through a film they both appear in, and repeat until they reach the target actor. The goal of the game is to reach the target actor in as few movie + actor combinations as possible. An alternate gamemode will be featured as well, in which players will once again choose movie + actor combinations to reach the target actor, but score higher the lower the total box office sales (adjusted for inflation) of their chosen movies is, incentivizing creative picks of less well-known movies over simply the shortest path to the target actor.

On the back-end of this web app, several datasets must be processed and synthesized to form the necessary web of connections between actors and movies: 1) a comprehensive dataset of movies and cast, 2) a list of corresponding box office sales, and 3) a dataset containing inflation indices for the relevant time frame. The information will be stored into efficient data structures and search algorithms will be created to determine optimal solutions for both game modes and scores will be given to players based on how far their selections deviate from the optimal.

Through the development of this web app, we seek to enforce strong data science and software engineering practices including: 1) data acquisition, cleaning, merging, and analysis, 2) unit testing and modular programming, 3) writing code and algorithms for game/app logic, and 4) designing a smooth UI experience with all of the data science and code abstracted away. We hope to provide an engaging and seamless game for users to enjoy.

## User Profile
### Casual movie enjoyer
Knows the most popular movies and actors, but has a shallow knowledge of indie actors and movies. Interested in challenging themselves and friends in a casual way. No programming knowledge is needed, but they will require an internet connection and the ability to browse the web while interacting with basic, standard, and intuitive web UI components.

### Avid cinema fan
Strong understanding of the world of cinema (knows an extensive amount of movies and actors), and interested in challenging their knowledge such as their awareness of indie titles and movies with low box office sales (in short, less popular titles). They potentially wish to compete with friends to see who the biggest movie connoisseur is. No programming knowledge is needed, but they will require an internet connection and the ability to browse the web while interacting with basic, standard, and intuitive web UI components.

### Game host (hypothetical/stretch goal, will not be part of component specifications or milestones for now until we have time to actually implement this)
Solid knowledge of movies and actors (knows a moderate amount of titles and actors), with an interest in setting up games for themself and/or friends for entertainment. They may wish to designate start and target actors for the game. No programming knowledge is needed, but they will require an internet connection and the ability to browse the web while interacting with basic, standard, and intuitive web UI components.

## Data Sources
### [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/)
Subsets of IMDb data are provided to customers for personal and non-commercial use. Each dataset is formatted as a gzipped, tab-separated-values (TSV) file in the UTF-8 character set. Each file’s first line is a header describing what is in each column, and a ‘/N’ denotes any missing or null fields. These datasets contain numerous variables, but are mainly focused on metadata such as titles, cast, genres, and ratings. As such, they do not include financial information.

### [Movie Revenues from Box Office Mojo](https://www.boxofficemojo.com/)
Box Office Mojo acts as a comprehensive source of box office performance data. By scraping box office collection revenue data from the site, we will be able to assign box office sales to each movie, and create the second, more challenging game mode incentivizing players to choose lower-revenue and less well-known titles.

### [U.S. Inflation Data from US Bureau of Labor Statistics](https://data.bls.gov/timeseries/CUUR0000SA0L1E?output_view=pct_12mths)
This dataset from the US Bureau of Labor Statistics includes monthly values of the Consumer Price Index for All Urban Consumers (CPI-U) in the US, from as far back as 1957. This data reflects the average CPI across all American cities for each month, with CPI being a critical economic aggregate indicator of the average change over time in prices paid by consumers for a representative “basket” of goods and services. In other words, it is a gauge of inflation, and will be used to adjust the revenues of movie titles for a fair comparison of popularity/success (otherwise older films would systematically be lower than newer films).

## Use Cases
### Casual movie enjoyer/Avid cinema fan
#### Objectives:
The avid cinema fan wants to entertain themselves with a game that challenges their knowledge of movies and actors. Specifically, they benefit from knowing more obscure titles.

#### Use case flow:
***User:*** Open app | Go to web link<br>
***System:*** Displays home screen with title, “Play Game” and “Instructions” buttons.

***User:*** See instructions | Presses “Instructions” button of home screen<br>
***System:*** Shows new page that includes text instructions, and back to home button.

***User:*** Play/choose game mode | Presses “Play Game” button of home screen<br>
***System:*** Screen with option to select either game mode, and back to home button.

***User:*** Choose challenge mode (lowest sum of box office sales) | Select “Challenge Mode: Obscure Titles” or similar label from game mode selection screen<br>
***System:*** Displays “Start Game” button and back to home button.

***User:*** Start the game | Press the “Start Game” button<br>
***System:*** Shows a random starting actor and random target actor, text input field asking for a movie, back to home button, and “New Game” button.

***User:*** Play a new game | Press the “New Game” button either during a game because they gave up, or upon finishing a game<br>
***System:*** Generates another random starting actor and random target actor, text input field asking for a movie, back to home button, and “New Game” button.

***User:*** Playing the game - Choosing a movie | Inputting a movie into text input field<br>
***System:*** Whenever the user inputs a movie title, the system checks if the movie is valid (the starting/current selected actor indeed appears in said movie). If the movie is invalid, the user is told the current actor does not appear in their selection, and must make a valid selection for the movie. If the movie is valid, the starting/current actor disappears from the screen and is replaced by the movie they selected, with a dropdown of the cast for that movie with a single name that can be selected. The target actor is still shown. Back to home screen button still available, along with “New Game” button.

***User:*** Playing the game - Choosing an actor | Selecting an actor from dropdown menu of a movie that includes list of cast<br>
***System:*** The current movie will be replaced by the selected actor (target actor still shown). The selected actor is now the current actor, and a text input field is displayed again, along with back to home button and “New Game” button.

***User:*** Playing the game - In general | Choosing movies or actors<br>
***System:*** Keeps alternating between showing the current movie or actor the user just selected, until either the user wins, or gives up and starts a new game/returns to the home screen/quits the app. They may use the corresponding buttons to start a new game or return to the home screen at any time. For more casual movie enjoyers who chose the base game mode, they are incentivized to pick whatever options they think will lead them to the target actor quickest. For more avid fans of cinema, who looked for a challenge in the challenge game mode, they must avoid high-revenue titles while still trying to get to the target actor as quickly as possible (inevitably, the more selections, the higher the total revenue will become, lowering their score).

***User:*** Wins the game | Selected the final movie + actor combination that leads to the target actor<br>
***System:*** Shows the target actor, with text indicating the user has won. A score is given based on how far from the optimal solution their series of selections were. We are still debating whether we should show the score live (throughout the game and changing whenever they make a new selection). A button offers to take them back to the home screen, while another button offers to start a new game.

***User:*** Starts a new game | Presses the “New Game” button from the winning screen<br>
***System:*** Shows a random starting actor and random target actor, text input field asking for a movie, back to home button, and “New Game” button.

***User:*** Return to the home screen | Presses home button (available on any screen except home screen itself)<br>
***System:*** Returns user to the home screen.

***Hypothetical if game host user case is implemented (stretch goal)***<br>
***User:*** Play a custom game created by a game host<br>
***System:*** New option in home screen to input a game key (key generated by game host and provided to players), leading them to start a new series of game(s) customized by the game host, who specified the number of games, custom starting/target actors, and which game mode.

### Game host (hypothetical/stretch goal, will not be implemented at first)
#### Objectives:
The game host wants to create game(s) for themselves or others to play, with the additional option to manually designate start and target actors rather than having them be random.

#### Use case flow:
***User:*** Start creating a custom series of game(s) | Press “Setup Game” button of home screen<br>
***System:*** Shows controls to customize 1) the number of games to be played, 2) who the starting and/or target actor(s) are (can still be kept random), and 3) which game mode is to be played. When the starting/target actors are specified, the system will calculate and display the optimal solution as well so the user can evaluate if their game seems too easy or difficult. If the starting/target actors are kept random, the game will randomly choose them BUT all players playing this series of game(s) will be assigned the exact same actors, allowing for players to directly compare their scores.

***User:*** Publish their custom series of game(s) | Press the “Publish Game and Generate Key” button<br>
***System:*** Tells the user if their game is a valid setup, and if so, generates a unique key for them to save and send to players and returns them back to the home screen. The settings specified by the game host and the corresponding key will be saved in the system. Anyone using the key in the future will load the customized series of game(s).
