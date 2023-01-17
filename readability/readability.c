#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// TO-DO: count letters (a-z, A-Z), count words (seperated by spaces), count sentences (seperated by periods, exclamation marks, question marks)
int *count(string s);
int grade(int *arr);
string letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

int main(void)
{
    string text = get_string("Text: ");
    int gr = grade(count(text));
    if (gr > 16)
    {
        printf("Grade 16+\n");
    }
    else if (gr < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", gr);
    }
}

// Returns array where arr[0] is the number of sentences aand arr[1] the number of words and arr[2] the number of letters. Grouped punctuation marks are counted as multiple sentences.
int *count(string s)
{
    // Iterate string and check for special characters that define words and sentences
    static int counters[3];

    for (int i = 0; i < strlen(s); i++)
    {
        char str[2];
        str[0] = s[i];
        str[1] = '\0';
        string match = strstr(letters, str);

        if ((s[i] == '.') || (s[i] == '!') || (s[i] == '?')) // Care: Grouped punctuation marks are counted as multiple sentences
        {
            counters[0]++; // Found a sentence
        }
        else if (s[i] == ' ')
        {
            counters[1]++; // Found a word
        }
        else if (match)
        {
            counters[2]++; //Found a letter
        }
    }
    // Increase number of words by one because number of spaces are counted
    if (strlen(s) > 0)
    {
        counters[1]++;
    }
    return counters;
}

// Calculates the reading level using the Coleman-Liau formula, rounded to the nearest integer
int grade(int *arr)
{
    double L = (double)(arr[2]) / arr[1] * 100;
    double S = (double)(arr[0]) / arr[1] * 100;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    return round(index);
}