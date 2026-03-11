import streamlit as st
import random
import time

page = st.sidebar.radio("Taya Na!", ["Color Game", "Shell Game", "About"])

if page == "Color Game":
    with st.container():
        st.title(" Color Game")
        player_name = st.text_input("Your name (optional):", key="player_name")
        difficulty = st.slider("Select difficulty (affects payout)", 1, 10, value=5)
        show_hints = st.checkbox("Show probability hints", key="color_hints")
        if show_hints:
            st.info("Each die has a 1/6 chance to match your selected color.")
        with st.expander("Game Rules"):
            st.write("Select a color and bet amount. Roll three dice. Win based on matches: 1 match = bet back, 2 matches = 2x bet, 3 matches = 3x bet. Difficulty affects payout multiplier.")

        colors = ['red', 'green', 'blue', 'yellow', 'white', 'pink']

    if 'money' not in st.session_state:
        st.session_state.money = 1000
    if 'bet_amount' not in st.session_state:
        st.session_state.bet_amount = 0
    if 'selected_color' not in st.session_state:
        st.session_state.selected_color = None
    if 'dice_results' not in st.session_state:
        st.session_state.dice_results = []
    if 'wins' not in st.session_state:
        st.session_state.wins = 0
    if 'losses' not in st.session_state:
        st.session_state.losses = 0

    st.subheader(f"Current Money: ${st.session_state.money}")
    st.metric("Wins", st.session_state.wins)
    st.metric("Losses", st.session_state.losses)

    if st.session_state.money <= 0:
        st.error("Game Over! You're out of money.")
        if st.button("Start New Game"):
            st.session_state.money = 1000
            st.session_state.bet_amount = 0
            st.session_state.selected_color = None
            st.session_state.dice_results = []
            st.session_state.message = ""
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.rerun()
    else:
        selected_color = st.selectbox("Select a color to bet on:", colors, index=colors.index(st.session_state.selected_color) if st.session_state.selected_color else 0)
        st.session_state.selected_color = selected_color

        st.session_state.bet_amount = st.slider("Select bet amount", 5, min(1000, st.session_state.money), value=st.session_state.bet_amount if st.session_state.bet_amount >= 5 else 5)
        st.metric(label="Current Funds", value=f"${st.session_state.money}", delta=f"${st.session_state.money - 1000}")

        if st.session_state.bet_amount > st.session_state.money:
            st.warning("You don't have enough money for this bet!")
        else:
            if st.button("Roll the Dice"):
                with st.spinner("Rolling the dice..."):
                    time.sleep(0.5)
                    st.session_state.dice_results = [random.choice(colors) for _ in range(3)]
                progress = st.progress(0)
                for i in range(1, 101, 25):
                    progress.progress(i)
                    time.sleep(0.05)

                matches = st.session_state.dice_results.count(st.session_state.selected_color)
                multiplier = 1 + (difficulty - 5) * 0.1  # higher difficulty = higher payout

                if matches == 0:
                    winnings = -st.session_state.bet_amount
                    msg = f"No matches! You lose ${st.session_state.bet_amount}."
                elif matches == 1:
                    winnings = int(st.session_state.bet_amount * multiplier)
                    msg = f"One match! You win ${winnings}."
                elif matches == 2:
                    winnings = int(2 * st.session_state.bet_amount * multiplier)
                    msg = f"Two matches! You win ${winnings}."
                elif matches == 3:
                    winnings = int(3 * st.session_state.bet_amount * multiplier)
                    msg = f"Three matches! You win ${winnings}."

                st.session_state.message = f"{player_name + ', ' if player_name else ''}{msg}"
                st.session_state.money += winnings
                if winnings > 0:
                    st.session_state.wins += 1
                elif winnings < 0:
                    st.session_state.losses += 1
                if matches > 0:
                    st.balloons()

        if st.session_state.dice_results:
            st.subheader("Dice Results:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Die 1: {st.session_state.dice_results[0]}")
            with col2:
                st.write(f"Die 2: {st.session_state.dice_results[1]}")
            with col3:
                st.write(f"Die 3: {st.session_state.dice_results[2]}")

            st.success(st.session_state.message)

            if st.button("Play Again"):
                st.session_state.dice_results = []
                st.session_state.message = ""
                st.rerun()

elif page == "Shell Game":
    with st.container():
        st.title("Shell Game")

        bowls = ['left', 'middle', 'right']

    if 'shell_selected_bowl' not in st.session_state:
        st.session_state.shell_selected_bowl = None
    if 'shell_rock_position' not in st.session_state:
        st.session_state.shell_rock_position = None
    if 'shell_revealed' not in st.session_state:
        st.session_state.shell_revealed = False
    if 'shell_message' not in st.session_state:
        st.session_state.shell_message = ""

    st.subheader(f"Current Money: ${st.session_state.money}")
    st.metric("Wins", st.session_state.wins)
    st.metric("Losses", st.session_state.losses)

    if st.session_state.money <= 0:
        st.error("Game Over! You're out of money.")
        if st.button("Start New Game"):
            st.session_state.money = 1000
            st.session_state.shell_selected_bowl = None
            st.session_state.shell_rock_position = None
            st.session_state.shell_revealed = False
            st.session_state.shell_message = ""
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.rerun()
    else:
        selected_bowl = st.selectbox("Select a bowl to find the rock:", bowls, index=bowls.index(st.session_state.shell_selected_bowl) if st.session_state.shell_selected_bowl else 0)
        st.session_state.shell_selected_bowl = selected_bowl

        st.session_state.bet_amount = st.slider("Select bet amount", 5, min(1000, st.session_state.money), value=st.session_state.bet_amount if st.session_state.bet_amount >= 5 else 5)

        if st.session_state.bet_amount > st.session_state.money:
            st.warning("You don't have enough money for this bet!")
        else:
            if st.button("Reveal Bowls"):
                st.session_state.shell_rock_position = random.choice(bowls)
                st.session_state.shell_revealed = True

                if st.session_state.shell_selected_bowl == st.session_state.shell_rock_position:
                    winnings = 2 * st.session_state.bet_amount
                    st.session_state.shell_message = f"Correct! The rock was under the {st.session_state.shell_rock_position} bowl. You win ${winnings}!"
                    st.session_state.money += winnings
                    st.session_state.wins += 1
                else:
                    st.session_state.money -= st.session_state.bet_amount
                    st.session_state.shell_message = f"Wrong! The rock was under the {st.session_state.shell_rock_position} bowl. You lose ${st.session_state.bet_amount}."
                    st.session_state.losses += 1

        if st.session_state.shell_revealed:
            st.subheader("Bowls:")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.session_state.shell_rock_position == 'left':
                    st.write("Left Bowl: 🪨 Rock!")
                else:
                    st.write("Left Bowl: Empty")
            with col2:
                if st.session_state.shell_rock_position == 'middle':
                    st.write("Middle Bowl: 🪨 Rock!")
                else:
                    st.write("Middle Bowl: Empty")
            with col3:
                if st.session_state.shell_rock_position == 'right':
                    st.write("Right Bowl: 🪨 Rock!")
                else:
                    st.write("Right Bowl: Empty")

            if st.session_state.shell_selected_bowl == st.session_state.shell_rock_position:
                st.success(st.session_state.shell_message)
            else:
                st.error(st.session_state.shell_message)

            if st.button("Play Again"):
                st.session_state.shell_selected_bowl = None
                st.session_state.shell_rock_position = None
                st.session_state.shell_revealed = False
                st.session_state.shell_message = ""
                st.rerun()

elif page == "About":
    with st.container():
        st.title("About")
    st.write("""The About page of the application describes its complete functionality through its use case demonstration. The application provides two carnival-style betting games through its color dice game and shell game which users can play for free. The application enables users to practice their betting techniques while playing interactive games which simulate the excitement of gambling without requiring actual monetary stakes.

The application which targets adult users who prefer casual gaming and casino-style entertainment and carnival games. The game suits people who want to play probability games and strategy games or who need a quick but interesting form of entertainment.

The system processes inputs and outputs through three essential elements Color Game The system processes inputs through three elements Color Game The system processes inputs through three elements Color Game users must select their desired color from six options and they need to place their bets between 5 and 1000 through three action buttons. The system displays current money information together with three dice colors and win/loss messages and game status.

The Shell Game system requires players to pick a bowl from three options and they need to place their bets between 5 and 1000 through three action buttons. The system displays current money information together with the revealed bowl contents which show the rock's location and win/loss messages and game status.""")
