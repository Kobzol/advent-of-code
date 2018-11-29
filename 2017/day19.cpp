#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

using Point = std::pair<int, int>;

Point moveDir(Point location, Point dir)
{
    return std::make_pair(location.first + dir.first, location.second + dir.second);
}
bool isNotEmpty(char data[200][200], Point location, Point dir)
{
    auto moved = moveDir(location, dir);
    if (moved.first >= 0 && moved.first < 200 && moved.second >= 0 && moved.second < 200)
    {
        return data[moved.first][moved.second] != ' ';
    }

    return false;
}

void day19()
{
    std::fstream input("input.txt");
    std::string line;

    char data[200][200];
    int counter = 0;
    int start = 77;
    while (std::getline(input, line))
    {
        for (int i = 0; i < line.size(); i++)
        {
            data[counter][i] = line[i];
        }
        counter++;
    }

    Point location{0, start};
    std::string sentence;
    Point dir{1, 0};

    int steps = 0;
    while (true)
    {
        auto moved = moveDir(location, dir);
        if (!(moved.first >= 0 && moved.first < 200 && moved.second >= 0 && moved.second < 200))
        {
            break;
        }
        location = moved;

        char c = data[location.first][location.second];
        if (isalpha(c))
        {
            sentence += c;
        }
        else if (c == '+')
        {
            if (dir.second == 0)
            {
                if (isNotEmpty(data, location, {0, 1}))
                {
                    dir = {0, 1};
                }
                else if (isNotEmpty(data, location, {0, -1}))
                {
                    dir = {0, -1};
                }
                else break;
            }
            else if (dir.first == 0)
            {
                if (isNotEmpty(data, location, {1, 0}))
                {
                    dir = {1, 0};
                }
                else if (isNotEmpty(data, location, {-1, 0}))
                {
                    dir = {-1, 0};
                }
                else break;
            }
        }
        else if (c != '|' && c != '-')
        {
            break;
        }

        steps++;
    }

    std::cout << steps << std::endl;
}
