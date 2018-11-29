#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

static std::string hashPos(int x, int y)
{
    return std::to_string(x) + "-" + std::to_string(y);
}

void day22()
{
    std::fstream input("input.txt");
    std::string line;

    std::unordered_map<std::string, int> infected;
    int row = 0;
    while (std::getline(input, line))
    {
        for (int i = 0; i < line.size(); i++)
        {
            if (line[i] == '#')
            {
                infected.insert({ hashPos(row, i), 2 });
            }
        }
        row++;
    }

    int infections = 0;
    std::pair<int, int> pos{ 12, 12, };
    std::pair<int, int> dirs[4] = {
            {-1, 0},
            {0, 1},
            {1, 0},
            {0, -1}
    };
    int dir = 0;

    for (int i = 0; i < 10000000; i++)
    {
        auto hash = hashPos(pos.first, pos.second);
        auto it = infected.find(hash);
        int state = 0;
        if (it != infected.end())
        {
            state = it->second;
        }

        if (state == 0)
        {
            dir = ((dir - 1) + 4) % 4;
            infected.insert({ hash, 1 });
        }
        else if (state == 1)
        {
            infected[hash]++;
            infections++;
        }
        else if (state == 2)
        {
            infected[hash]++;
            dir = (dir + 1) % 4;
        }
        else
        {
            infected.erase(hash);
            dir = (dir + 2) % 4;
        }

        pos.first += dirs[dir].first;
        pos.second += dirs[dir].second;
    }

    std::cout << infections << std::endl;
}
