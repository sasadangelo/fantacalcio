import csv

# Parameters
K = 30  # Adjustment coefficient

# Function to calculate the win probability
def calculate_probability(rating_A, rating_B):
    return 1 / (1 + 10 ** ((rating_B - rating_A) / 400))

# Function to update the rating
def update_rating(rating_A, rating_B, result_A):
    prob_A = calculate_probability(rating_A, rating_B)
    new_rating_A = rating_A + K * (result_A - prob_A)
    return new_rating_A

# Load initial ratings or create a new table
def load_team_ratings(teams):
    ratings = {}
    for team in teams:
        ratings[team] = 1500
    return ratings

# Update the team ratings based on match results
def process_matches(matches_file, ratings_file):
    # Read the matches
    with open(matches_file, 'r') as f:
        reader = csv.DictReader(f)
        matches = list(reader)

    # Find all teams
    teams = set()
    for match in matches:
        teams.add(match['Team A'])
        teams.add(match['Team B'])

    # Load or initialize ratings
    ratings = load_team_ratings(teams)

    # Process each match
    for match in matches:
        team_A = match['Team A']
        team_B = match['Team B']
        result = match['Result'].split('-')
        goals_A = int(result[0])
        goals_B = int(result[1])

        # Determine the match outcome
        if goals_A > goals_B:
            result_A = 1
            result_B = 0
        elif goals_A < goals_B:
            result_A = 0
            result_B = 1
        else:
            result_A = 0.5
            result_B = 0.5

        # Calculate the new ratings
        new_rating_A = update_rating(ratings[team_A], ratings[team_B], result_A)
        new_rating_B = update_rating(ratings[team_B], ratings[team_A], result_B)

        # Update the ratings
        ratings[team_A] = new_rating_A
        ratings[team_B] = new_rating_B

    # Write the results to the ratings file
    with open(ratings_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Team', 'Rating'])
        for team, rating in sorted(ratings.items()):
            writer.writerow([team, round(rating, 2)])

# Run the script
if __name__ == "__main__":
    process_matches('matches.csv', 'ratings.csv')
