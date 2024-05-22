# Mafia: The Ultimate Social Deduction Game

Welcome to Mafia, a thrilling social deduction game where deception and strategy are key to survival. This game is developed using HTML, CSS, and JavaScript, with a Flask backend hosted on Vercel. Playable on both mobile and desktop screens, Mafia offers an engaging experience for all players. The game includes sound effects to enhance the experience, with audio cues for kills, votes, and other key moments.

## Game Rules

### Roles

1. **Mafia (Killer)** - Kills one person per night.
   
2. **Doctor** - Saves one person per night.
   
3. **Police** - Investigates one person per night to determine if they are the Mafia.
   
4. **Prankster** - Pranks one person per night, preventing them from using their power.
   
5. **Civilian (Villager)** - A normal villager with no special powers.

## Game Flow

<details>
  <summary>Joining the Game</summary>
  <p>Enter your name and join a room. You can create a new room or join an existing one. The host will start the game, and each player will receive a role card.</p>
</details>

<details>
  <summary>Night Phase</summary>
  <p>Depending on your role, you will perform the following actions:</p>
  <ul>
    <li><strong>Mafia</strong>: Choose one player to kill.</li>
    <li><strong>Doctor</strong>: Choose one player to save.</li>
    <li><strong>Police</strong>: Choose one player to investigate.</li>
    <li><strong>Prankster</strong>: Choose one player to prank.</li>
    <li><strong>Civilian</strong>: Your choice does not affect the game.</li>
  </ul>
</details>

<details>
  <summary>Day Phase</summary>
  <ul>
    <li><strong>Discussion Round</strong>: Players discuss who they think the Mafia is.</li>
    <li><strong>Voting Round</strong>: Players vote on who they think the Mafia is.</li>
    <li><strong>Voting Results</strong>: If the Mafia is voted out, the game ends. If not, the game continues to the next night phase.</li>
  </ul>
</details>

### Winning the Game

The game continues until either the Mafia is voted out or the Mafia successfully kills all other players.

## How to Play

1. **Start the Game**
   - Visit the game link [here](#).
   - Enter your name and join a room.
   
2. **Host Starts the Game**
   - The host starts the game, and roles are distributed.
   
3. **Night and Day Phases**
   - Follow the instructions based on your role.
   - Discuss, vote, and try to deduce who the Mafia is.

## Sound Effects

The game features various sound effects to make the experience more engaging:
- **Kill Sound**: Plays when someone is killed at night.
- **Vote Sound**: Plays during the voting phase.
- **Elimination Sound**: Plays when someone is voted out.

## Flow Diagram

For a visual representation of the game flow and states, refer the diagram given below.
<img width="2030" alt="Mafia Design" src="https://github.com/meet244/Mafia/assets/83262693/ae43634a-31ef-423c-8545-6b35ac68756d">


## Background

The game was inspired by the traditional Mafia game played with friends using chats and a human host. This digital version automates the process, making it faster and more convenient, allowing everyone to participate without the need for a dedicated host.

## Contribution

If you encounter any issues or have suggestions for improvements, feel free to raise an issue or contribute to the project.

---

Thank you for playing Mafia! Enjoy the game and may the best detective win.
