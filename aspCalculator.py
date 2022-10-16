INTEREST_ORDER = ['Politics', 'Money', 'Environment',
                  'Crime', 'Entertainment', 'Culture',
                  'Food', 'Health', 'Fashion',
                  'Sports', 'Paranormal', 'Travel',
                  'Work', 'Weather', 'Animals',
                  'School', 'Toys', 'Sci-Fi']


def calculate_aspiration_values(interests):
    # knowledge: 2x paranormal, work, environment, sci-fi
    knowledge_score = 2 * interests[10] + interests[12] + interests[2] + interests[17]
    # family: 2x food, toys, animals, school
    family_score = 2 * interests[6] + interests[16] + interests[14] + interests[15]
    # popularity: 2x travel, culture, sports, weather
    popularity_score = 2 * interests[11] + interests[5] + interests[9] + interests[13]
    # romance: 2x fashion, health, travel, entertainment
    romance_score = 2 * interests[8] + interests[7] + interests[11] + interests[4]
    # pleasure: 2x entertainment, food, culture, fashion
    pleasure_score = 2 * interests[4] + interests[6] + interests[5] + interests[8]
    # fortune: 2x money, politics, crime, work
    fortune_score = 2 * interests[1] + interests[0] + interests[3] + interests[12]
    scores = [('Knowledge', knowledge_score), ('Family', family_score),
              ('Popularity', popularity_score), ('Romance', romance_score),
              ('Pleasure', pleasure_score), ('Fortune', fortune_score)]
    scores.sort(key=lambda tup: tup[1], reverse=True)

    return scores
