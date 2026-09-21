# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [The game's purpose is to aid at guessing a number from a given range. You have a limited amount of guesses and as you guess you get feedback on whther to go higher or lower inn order to guess the secret number.]
- [ ] Detail which bugs you found.

  1. **The hints were backwards.** When your guess was too high the game told you to go HIGHER, and when it was too low it told you to go LOWER. Following the hints walked you away from the answer.
  2. **The secret was turned into a string every other turn.** On even-numbered attempts the code did `secret = str(secret)`, so it was comparing a number to a piece of text. Python raised a `TypeError`, which triggered a fallback that compared them alphabetically instead of numerically. Alphabetically `"9"` comes after `"80"`, so guessing 9 when the secret was 80 told you that you were too high.
  3. **That `TypeError` fallback was hiding the real bug.** It caught the error so nothing ever crashed, which made the wrong hints look like random bad luck instead of a broken comparison.
  4. **New Game didn't actually start a new game.** It reset the attempts and the secret but never reset `status`, so after you won or lost once the status check ran `st.stop()` on every rerun and you were locked out for good. It also kept your old score and guess history.
  5. **New Game ignored the difficulty.** It always rolled a number from 1 to 100, so on Easy (range 1-20) it could pick something like 87 that you could never reach.
  6. **All the logic lived in `app.py` and `logic_utils.py` was empty**, so none of the tests could run.

- [ ] Explain what fixes you applied.

  - **Swapped the hint messages** so "Too High" tells the player to go LOWER and "Too Low" tells them to go HIGHER. I had to fix this in two places, because the same mistake appeared in the `TypeError` fallback as well.
  - **Deleted the `secret = str(secret)` cast.** The secret now stays an integer on every turn, so the comparison is always numeric.
  - **Deleted the `TypeError` fallback.** Once the cast was gone, that code could never run. It was never a real safety net, it was just covering up the bug, and the alphabetical comparison inside it was wrong anyway.
  - **Made New Game reset everything**: `status` back to `"playing"`, plus score and history. Resetting `status` is what actually unlocks the game.
  - **Made New Game use `randint(low, high)`** so the secret always falls inside the range for the difficulty you picked.
  - **Moved all four functions into `logic_utils.py`** and imported them into `app.py`. They are plain Python with no Streamlit in them, which is what lets pytest call them directly.
  - **Changed `check_guess` to return just the outcome** (`"Win"`, `"Too High"`, `"Too Low"`) instead of a tuple of `(outcome, message)`. The tests compare against a plain string, and a tuple never equals a string, so they could not have passed otherwise. A separate `get_hint()` function turns an outcome into the emoji message. Keeping the message in a function means a test can check the hint direction; if it had stayed in `app.py` nothing could catch it being flipped again.
  - **Added 12 tests** on top of the 3 that came with the starter. The most useful ones pin the alphabetical-comparison bug directly: `check_guess(9, 80)` must return "Too Low", which is exactly the case that used to fail.

  **What I learned:** most of these come down to how Streamlit works. It re-runs the whole script top to bottom every time you click anything, so ordinary variables reset constantly and `st.session_state` is the only thing that remembers between runs. The New Game bug was really a session-state bug: the reset simply forgot one of the five things it needed to clear.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Think of a number from 1-100 and type it into the inbox and submit-->
2. <!-- Make sure you are looking at the hint to continue guessing and choose another number higher or lower and submit -->
3. <!-- Continue repeating step two until the guess is correct -->
4. <!-- Click new game to reset the game with a new number -->
5. <!-- Repeat steps 1-4 and play as many games as you want! -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
