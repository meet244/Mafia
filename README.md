![Frame 22](https://github.com/meet244/Mafia/assets/83262693/68fa0e70-b5c8-43f4-93fb-efc360e67c5f)

[Mafia](https://mafia-play.vercel.app/) is a thrilling social deduction game where deception and strategy are key to survival. This game is developed using HTML, CSS, and JavaScript, with a Flask backend hosted on Vercel. Playable on both mobile and desktop screens, Mafia offers an engaging experience for all players. The game includes sound effects to enhance the experience, with audio cues for kills, votes, and other key moments.

## Game Rules

### Roles

1. **Mafia (Killer)** - Kills one person per night.
   
2. **Doctor** - Saves one person per night.
   
3. **Police** - Investigates one person per night to determine if they are the Mafia.
   
4. **Prankster** - Pranks one person per night, preventing them from using their power.
   
5. **Civilian (Villager)** - A normal villager with no special powers.

## Game Flow

### Joining the Game
Go to [MAFIA website](https://mafia-play.vercel.app/). Enter your name and join a room. You can create a new room or join an existing one. The host will start the game, and each player will receive a role card.

### Night Phase
Depending on your role, you will perform the following actions:
- **Mafia**: Choose one player to kill.
- **Doctor**: Choose one player to save.
- **Police**: Choose one player to investigate.
- **Prankster**: Choose one player to prank.
- **Civilian**: Your choice does not affect the game.

### Day Phase
- **Discussion Round**: Players discuss who they think the Mafia is.
- **Voting Round**: Players vote on who they think the Mafia is.
- **Voting Results**: If the Mafia is voted out, the game ends. If not, the game continues to the next night phase.


### Winning the Game

The game continues until either the Mafia is voted out or the Mafia successfully kills all other players.

## Screenshots

<details>
   <br>
  <summary><strong>Mobile</strong></summary>
<img src="https://github.com/meet244/Mafia/assets/83262693/20c65a19-f29e-4ded-ad7d-97833a70d580" alt="m1" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/87425abb-d817-41e2-93ff-5eba419abed2" alt="m2" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/27856265-0eba-4b90-b81f-26fd1450a231" alt="m3" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/fbaec60e-cc3f-4b3d-aa22-d49e34255a16" alt="m4" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/fa6c620e-da80-4fb0-be58-6019c81dc700" alt="m5" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/da46f970-343f-44e7-98ca-4e1bbd83366f" alt="m6" height="430" width="216" />
<img src="https://github.com/meet244/Mafia/assets/83262693/e82159e8-c28a-47ca-a151-473dce26671d" alt="m7" height="430" width="216" />
   
</details>
<details>
   <br>
  <summary><strong>Desktop</strong></summary>
  
<img src="https://github.com/meet244/Mafia/assets/83262693/de9758fe-d2e5-480e-8b21-e3f7758f2b48" alt="pc1" />
<img src="https://github.com/meet244/Mafia/assets/83262693/1f40bcbf-2752-4b21-973f-a79fca522d23" alt="pc2" />
<img src="https://github.com/meet244/Mafia/assets/83262693/662dbb6a-bd74-4eff-a33b-8cfa29c36121" alt="pc3" />  
<img src="https://github.com/meet244/Mafia/assets/83262693/e1d49f30-5e6b-42fa-b548-f42bad96d6f6" alt="pc4" /> 
   
</details>

## Game Flow Diagram

For a visual representation of the game flow and states, refer the diagram given below.
<br>
<br>
![image 10 (1)](https://github.com/meet244/Mafia/assets/83262693/8fdae7c7-2166-42dd-b2cf-96af50b67f81)

## Game Designs

<details>
  <summary><strong>Website designs (low fidelity):</strong></summary>
  <br>
      <img src="https://github.com/meet244/Mafia/assets/83262693/a9f0a62f-2d0d-414d-b5ea-0031236d86fa" alt="Designs (low fidelity)"/>
</details>

## Background

The game was inspired by the traditional Mafia game played with friends using chats and a human host. This digital version automates the process, making it faster and more convenient, allowing everyone to participate without the need for a dedicated host.

<details>
  <summary><strong>How we used to play...</strong></summary>
  <br>
<p>We used to make <strong>paper chits or cards</strong>, and in those chits, we would write the names of the roles like Civilian, Mafia, Police, and others. These chits were then distributed among the players. There would be a <strong>god or a host who controlled the entire game</strong>. The host would ask everyone to <strong>close their eyes</strong>, then call on the Mafia to open their eyes and choose someone to kill. Afterward, the Doctor would open their eyes and choose someone to save. The <strong>game was very sequential</strong>, with each role acting one after another, making the process <strong>quite lengthy</strong> and sometimes <strong>frustratingly slow</strong>. The entire game took a lot of time.</p>
<p>Additionally, some players used to <strong>cheat between rounds</strong>, trying to gain an advantage by <strong>peeking or signaling to each other</strong>. This added an extra layer of challenge and suspicion to the game.</p>

   <img src="https://github.com/meet244/Mafia/assets/83262693/344a2363-2f8d-480e-bb34-4014dd332fe1" alt="Chits game"/>
</details>

## Contribution

If you encounter any issues or have suggestions for improvements, feel free to raise an issue or contribute to the project.

---

Thank you for playing Mafia! Enjoy the game and may the best detective win.
