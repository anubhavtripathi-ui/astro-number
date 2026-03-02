def get_personality_and_enemy(mulank):
    data = {
        1: ("Natural leader, ambitious and independent.", 8),
        2: ("Emotional, diplomatic and intuitive.", 7),
        3: ("Creative, expressive and optimistic.", 6),
        4: ("Practical, disciplined and hardworking.", 9),
        5: ("Adventurous, dynamic and adaptable.", 2),
        6: ("Responsible, caring and balanced.", 3),
        7: ("Analytical, spiritual and thoughtful.", 2),
        8: ("Powerful, goal-driven and authoritative.", 1),
        9: ("Compassionate, humanitarian and wise.", 4),
    }

    personality, enemy = data.get(mulank, ("Data unavailable.", "N/A"))
    return personality, enemy
