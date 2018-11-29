#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

float calculateDistance(float x, float y)
{
    return std::abs(x) + (y - std::abs(x) / 2.0f);
}

void day11()
{
    std::fstream input("input.txt");
    std::string line;
    std::getline(input, line);

    float x = 0;
    float y = 0;
    float distance = 0.0f;
    for (int i = 0; i < line.size(); i++)
    {
        std::string dir;
        while (i < line.size() && line[i] != ',')
        {
            dir += line[i];
            i++;
        }

        if (dir == "n")
        {
            y++;
        }
        else if (dir == "s")
        {
            y--;
        }
        else if (dir == "se")
        {
            y -= 0.5f;
            x++;
        }
        else if (dir == "sw")
        {
            y -= 0.5f;
            x--;
        }
        else if (dir == "ne")
        {
            y += 0.5f;
            x++;
        }
        else if (dir == "nw")
        {
            y += 0.5f;
            x--;
        }

        distance = std::max(distance, calculateDistance(x, y));
    }

    std::cout << x << " " << y << " " << calculateDistance(x, y) << std::endl;
    std::cout << distance << std::endl;
}
