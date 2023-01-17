#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool validate_key(string s);
char *generate_ciphertext(string text, string key);

int main(int argc, string argv[])
{
    // Check for correct command line usage
    if ((argc == 1) || (argc > 2))
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Check for right key length and content
    string key = argv[1];
    if (!validate_key(key))
    {
        return 1;
    }

    // Read user input for plaintext
    string plaintext = get_string("plaintext: ");

    // Print ciphertext
    string ciphertext = generate_ciphertext(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}

// Substitute every char in the plaintext with the corresponding char
// in the key provided by the user while preserving upper-, lowercase
char *generate_ciphertext(string text, string key)
{
    char *result = malloc(strlen(text));
    // Iterate the text and add the corresponding char from key to result
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (islower(c))
        {
            int key_index = c - 97;
            result[i] = tolower(key[key_index]);
        }
        else if (isupper(c))
        {
            int key_index = c - 65;
            result[i] = toupper(key[key_index]);
        }
        else
        {
            result[i] = text[i]; // Whitespace and non-alphabetical characters stay the same
        }
    }
    return result;
}

// Check if key is 26 chars long and contains only a-z only once
bool validate_key(string s)
{
    // Check for right length
    if (strlen(s) != 26)
    {
        printf("Key must be 26 characters long!\n");
        return 0;
    }

    // Check for alphabetical content
    for (int i = 0; i < strlen(s); i++)
    {
        char c = s[i];
        if (!isalpha(c))
        {
            printf("Key must contain only alphabetical characters!\n");
            return 0;
        }
    }

    // Check for duplicate chars
    char content[26]; // Will contain a record of occurring chars in s
    for (int i = 0; i < strlen(s); i++)
    {
        char c = s[i];
        // Iterate through content and compare c to every entry
        for (int j = 0; j < 26; j++)
        {
            if (content[j] == c)
            {
                // Duplicate found
                printf("No duplicate characters are allowed!\n");
                return 0;
            }
        }
        content[i] = c; // Add c to content for next iterations
    }

    return 1; // We return true when all conditions are met
}