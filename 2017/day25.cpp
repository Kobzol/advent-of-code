#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

void day25()
{
    std::fstream input("input.txt");
    std::string line;

    while (std::getline(input, line))
    {

    }

    std::unordered_map<int, int> tape;
    int position = 0;
    int state = 0;
    for (int i = 0; i < 12302209; i++)
    {
        int val = tape[position];
        if (state == 0)
        {
            if (val == 0)
            {
                tape[position] = 1;
                position++;
                state = 1;
            }
            else
            {
                tape[position] = 0;
                position--;
                state = 3;
            }
        }
        else if (state == 1)
        {
            if (val == 0)
            {
                tape[position] = 1;
                position++;
                state = 2;
            }
            else
            {
                tape[position] = 0;
                position++;
                state = 5;
            }
        }
        else if (state == 2)
        {
            if (val == 0)
            {
                tape[position] = 1;
                position--;
                state = 2;
            }
            else
            {
                tape[position] = 1;
                position--;
                state = 0;
            }
        }
        else if (state == 3)
        {
            if (val == 0)
            {
                tape[position] = 0;
                position--;
                state = 4;
            }
            else
            {
                tape[position] = 1;
                position++;
                state = 0;
            }
        }
        else if (state == 4)
        {
            if (val == 0)
            {
                tape[position] = 1;
                position--;
                state = 0;
            }
            else
            {
                tape[position] = 0;
                position++;
                state = 1;
            }
        }
        else if (state == 5)
        {
            if (val == 0)
            {
                tape[position] = 0;
                position++;
                state = 2;
            }
            else
            {
                tape[position] = 0;
                position++;
                state = 4;
            }
        }
    }

    int count = 0;
    for (auto& place : tape)
    {
        if (place.second == 1) count++;
    }
    std::cout << count << std::endl;
}
