#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(void)
{
    // Save user input, must be the right length for a credit card number. Exit if not.
    long nmb = get_long("Number: ");
    if (nmb < (pow(10, 12)) || nmb > 9999999999999999)
    {
        printf("INVALID\n");
        exit(0);
    }
    //-------------------------------------------------------------------------------------
    // Luhn's algorithm determines whether the entered number could be a credit card number
    long n = nmb;
    long dgt;
    long sum = 0;
    bool flip = false;

    // Iterate through the credit card number using % and /
    while (n > 0)
    {
        dgt = n % 10; // We look at the least sigificant digit
        if (flip)
        {
            dgt = dgt * 2; // Double every second digit
        }
        // Add up the digits (per digit --> 12 becomes 1 and 2)
        if (dgt > 9)
        {
            sum = sum + (dgt - 9); // e.g 12 becomes 3 (1+2)
        }
        else
        {
            sum = sum + dgt;
        }
        n = n / 10; // Remove added digit from the remaining credit card number digits
        flip = !flip;
    }
    // Luhn finished
    //-------------------------------------------------------------------------------------

    string type = "INVALID";
    // Determine the card provider by looking at the starting digits
    if ((sum % 10) == 0)
    {
        if (((long)(nmb / pow(10, 13)) == 34) || ((long)(nmb / pow(10, 13)) == 37))
        {
            type = "AMEX";
        }
        if (((long)(nmb / pow(10, 14)) >= 51) && ((long)(nmb / pow(10, 14))) <= 55)
        {
            type = "MASTERCARD";
        }
        if (((long)(nmb / pow(10, 15)) == 4) || ((long)(nmb / pow(10, 12)) == 4))
        {
            type = "VISA";
        }
    }
    // Finally, print out the card provider
    printf("%s\n", type);
}