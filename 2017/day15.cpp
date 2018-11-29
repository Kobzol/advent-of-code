#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>
#include <queue>

void day15()
{
    size_t generators[2] = { 873, 583 };
    size_t factors[2] = { 16807, 48271 };
    std::queue<size_t> numbers[2];

    int count = 0;
    int pairs = 0;
    while (true)
    {
        for (int j = 0; j < 2; j++)
        {
            generators[j] *= factors[j];
            generators[j] %= 2147483647;
        }

        if (generators[0] % 4 == 0) numbers[0].push(generators[0]);
        if (generators[1] % 8 == 0) numbers[1].push(generators[1]);

        while (!numbers[0].empty() && !numbers[1].empty())
        {
            size_t a = numbers[0].front();
            numbers[0].pop();
            size_t b = numbers[1].front();
            numbers[1].pop();

            if ((a & 0xFFFF) == (b & 0xFFFF))
            {
                count++;
            }

            pairs++;
            if (pairs == 5000000) break;
        }

        if (pairs >= 5000000) break;
    }

    std::cout << count << std::endl;
}
