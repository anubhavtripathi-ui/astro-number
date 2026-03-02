def get_personality(mulank):
    personality_dict = {
        1: "Natural leader, ambitious, independent and confident.",
        2: "Emotional, diplomatic, intuitive and cooperative.",
        3: "Creative, expressive, optimistic and social.",
        4: "Practical, disciplined, stable and hardworking.",
        5: "Adventurous, dynamic, freedom-loving and adaptable.",
        6: "Responsible, caring, family-oriented and balanced.",
        7: "Analytical, spiritual, introspective and thoughtful.",
        8: "Powerful, goal-driven, authoritative and determined.",
        9: "Compassionate, humanitarian, generous and wise."
    }

    return personality_dict.get(mulank, "Personality data unavailable.")