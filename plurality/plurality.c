#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    bool found_candidate;
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            //Found the candidate voted for. Increase his votes.
            found_candidate = true;
            candidates[i].votes++;
        }
    }
    // String name not a valid name. Do not change anything.
    if (found_candidate == false)
    {
        return false;
    }
    return true;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // Sort the most voted candidate to the first index of the candidate array
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[0].votes < candidates[i].votes)
        {
            // Swap
            candidate tmp = candidates[0];
            candidates[0] = candidates[i];
            candidates[i] = tmp;
        }
    }

    // Print the winners name
    printf("%s\n", candidates[0].name);

    // Look at possible tie if more than one candidate was listed
    if (candidate_count > 1)
    {
        candidate add_winners[candidate_count];
        int ties = 0;
        for (int i = 1; i < candidate_count; i++) // No need to look at the winner at index 0
        {
            if (candidates[i].votes == candidates[0].votes)
            {
                // If the candidate has the same amount of votes as the winner, add him to the list of additional winners
                add_winners[i] = candidates[i];
                ties++;
            }
            else
            {
                // Mark the empty spots in the add_winners array by setting their names to "loser"
                add_winners[i].name = "loser";
            }
        }
        // In case of a tie print out all additional winner's names
        if (ties > 0)
        {
            for (int i = 1; i < candidate_count; i++)
            {
                // Use the mark we left earlier to filter out the names we need to print
                if (strcmp("loser", add_winners[i].name) != 0)
                {
                    printf("%s\n", add_winners[i].name);
                }
            }
        }
    }
    return;
}