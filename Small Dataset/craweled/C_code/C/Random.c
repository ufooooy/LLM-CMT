#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    unsigned char seed = 100;
    srand(seed);
    int random_number = rand();
    printf("Random: %d\n", random_number);
    return 0;
}
