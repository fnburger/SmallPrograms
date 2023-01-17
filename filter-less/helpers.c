#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the average value of the three channels and set all three channels to this grayscale value
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.00);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int m = 255;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate sepia values using common values
            int sepiaRed = round(image[i][j].rgbtRed * 0.393 +
                                 image[i][j].rgbtGreen * 0.769 +
                                 image[i][j].rgbtBlue * 0.189);
            int sepiaGreen = round(image[i][j].rgbtRed * 0.349 +
                                   image[i][j].rgbtGreen * 0.686 +
                                   image[i][j].rgbtBlue * 0.168);
            int sepiaBlue = round(image[i][j].rgbtRed * 0.272 +
                                  image[i][j].rgbtGreen * 0.534 +
                                  image[i][j].rgbtBlue * 0.131);
            // Make sure no channel is above the max of 255
            image[i][j].rgbtRed = sepiaRed > m ? m : sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen > m ? m : sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue > m ? m : sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        if (width % 2 == 0)
        {
            for (int j = 0; j < width / 2; j++)
            {
                // Swap values in each row from left to right and vice versa
                RGBTRIPLE temp[height][width];
                temp[i][j] = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = temp[i][j];
            }
        }

        else if (width % 2 != 0)
        {
            for (int j = 0; j < (width - 1) / 2; j++)
            {
                RGBTRIPLE temp[height][width];
                temp[i][j] = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = temp[i][j];
            }
        }
    }
    return;
}

// Helper function, gets called for each channel for each pixel. returns average of the neighbouring pixels with radius 1
int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int channel)
{
    float counter = 0;
    int sum = 0;

    for (int k = i - 1; k < (i + 2); k++) // radius is 1
    {
        for (int l = j - 1; l < (j + 2); l ++) // radius is 1
        {
            // If the pixel is outside the images' borders don't do anything
            if (k < 0 || l < 0 || k >= height || l >= width)
            {
                continue;
            }
            if (channel == 0)
            {
                sum += image[k][l].rgbtRed;
            }
            else if (channel == 1)
            {
                sum += image[k][l].rgbtGreen;
            }
            else
            {
                sum += image[k][l].rgbtBlue;
            }
            counter++;

        }
    }
    return round(sum / counter);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    // Populate the copy of the image with a copy of all values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    // Set the values to the averages of their neighbours within a radius of 1 pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = getBlur(i, j, height, width, copy, 0);
            image[i][j].rgbtGreen = getBlur(i, j, height, width, copy, 1);
            image[i][j].rgbtBlue = getBlur(i, j, height, width, copy, 2);
        }
    }
    return;
}
