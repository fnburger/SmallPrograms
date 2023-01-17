#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // Open existing file
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Declare variables
    typedef uint8_t BYTE;
    BYTE *buffer = malloc(sizeof(BYTE) * 512);
    int files_found = 0;
    char filename[8];
    FILE *current_file = NULL;

    // Read 512 byte block into buffer and repeat until end of input file
    while (fread(buffer, 512, 1, f) == 1)
    {
        // If is beginning of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (files_found != 0) // If is not first JPEG close old file
            {
                fclose(current_file);
            }
            // Initialise file and increment counter
            sprintf(filename, "%03i.jpg", files_found++); // Allocates a formated string in memory
            current_file = fopen(filename, "w");
        }
        if (files_found != 0)  // If JPEG is found, write
        {
            fwrite(buffer, 512, 1, current_file);
        }
    }
    
    // Close remaining files
    fclose(current_file);
    fclose(f);
    // Free allocated memory and exit
    free(buffer);
    return 0;
}