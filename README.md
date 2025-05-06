#### By Diaconescu Stefania Clara and Postelnicu Cristina-Marina

## Description

TriviaWorld is an interactive trivia game that has 10 leveles, each contaning
5 randomly selected questions from a predefined database, `questions.json`.
If a player answers correctly to all the questions in every level without
making any mistakes, they successfully win the game.

The game uses a grafical interface built using `tkinter`, the standard Python
library for creating graphical user interfaces. This library is used to create
the main game window, buttons, labels and other elements. Also, this
implementation uses the `Pilow library` for image manipulation in order to
provide an image as a background for the game.

## Implementation

The project contains functions that parse the questions and a class that provides
the functionalities of the game itself:

- `load_questions`

    This function loads the questions from the questions.json file, the
    `json.load(f)` function reads the content of the file and converts it into
    a Python list of dictionaries, where each dictionary represents a question.
    The questions are stored in the global variable `all_questions`.

- `get_random_questions`
    This function is used at the beginning of each level to generate the
    questions for that level. It selects 5 questions using the `random` module.

- `TriviaWorlds Class`

    - `__init__` 
        This method is used to initialize the main game window, sets its
        dimensions and properties and loads the background image. It also
        initializes variables like: current_level, correct_answers, that keeps
        count of the correct answers given by the player in the current level,
        level_status, a list that stores the status of each level, passed or
        failed, and is used to update the level map and check if the game is
        completed.

    - `_on_resize_`
        This method dynamically resizes the background image when the window is
        resized. The image is adjusted to fit the current window dimensions.

    - `show_start_screen`
        This method displays the start screen of the game. It clears the current
        screen, sets the background and shows a welcome message along with a
        "Start Game" button.

    - `show_level_map`
        This method displays the level map, allowing the player to select a level.
        It creates buttons for each level and organizes them in a grid. The
        buttons' colors are updated based on the status of each level, the passed
        levels are green and the faild ones are red.

    - `start_level`
        This method initializes a new level. It sets the current level, resets
        the correct answers counter, selects random questions for the level using
        `get_random_questions` and displays the first question.

    - `show_question`
        This method displays the current question and its answer options. It
        creates radio buttons for the player to select an answer and a "Submit
        Answer" button to validate the selection. If all questions in the level
        are answered, it calls `finish_level`.

    - `check_answer`
        This method checks the player's selected answer against the correct
        answer. If the answer is correct, it increments the correct answers
        counter. If incorrect, it displays the correct answer. Afterward, it
        moves to the next question or finishes the level.

    - `finish_level`
        This method finalizes the current level. It determines if the player has
        passed or failed the level based on the number of correct answers. It
        updates the level status and displays a message indicating success or
        failure. If all levels are passed, it calls `show_victory_animation`.

    - `start_next_level`
        This method automatically starts the next level if available. If all
        levels are completed, it calls `show_victory_animation`.

    - `create_confetti`
        This method generates confetti for the victory animation. It creates
        small colored shapes that fall from the top of the screen to simulate
        confetti.

    - `animate_confetti`
        This method animates the confetti created by `create_confetti`. It moves
        the confetti shapes downward and resets their position when they fall
        off the screen.

    - `show_victory_animation`
        This method displays a congratulatory message and triggers the confetti
        animation when the player completes all levels successfully.

    - `update_level_colors`
        This method updates the colors of the level buttons on the level map
        based on their status. Passed levels are green, failed levels are red,
        and unattempted levels are gray.

    - `clear_screen`
        This method removes all widgets from the screen except the background
        image. It is used to prepare the screen for new content.

    - `set_background`
        This method sets the background image for the game. It ensures the
        background is displayed behind all other widgets.
