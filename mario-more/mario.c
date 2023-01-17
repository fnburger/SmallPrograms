#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Read user input, must be between 1 and 8 (inclusive)
    int height = 0;
    while (height > 8 || height < 1)
    {
        height = get_int("Height: ");
    }

    //Print stairs
    int counter = 1;
    for (int i = 0; i < height; i++) //one iteration is one line
    {
        //Print spaces for each line
        for (int j = 0; j < height - counter; j++)
        {
            printf(" ");
        }
        //Print left side of stairs
        for (int j = 0; j < counter; j++)
        {
            printf("#");
        }

        printf("  "); //Make the gap

        //Print right side of stairs
        for (int j = 0; j < counter; j++)
        {
            printf("#");
        }

        printf("\n"); //Enter the next line
        counter++; //increment number of blocks
    }
}