#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>

void day5()
{
    std::fstream input("input.txt");
    std::string line;

    std::vector<int> jumps;
    while (std::getline(input, line))
    {
        jumps.push_back(std::strtol(line.c_str(), nullptr, 10));
    }

    size_t index = 0;
    size_t steps = 0;
    while (index >= 0 && index < jumps.size())
    {
        long offset = jumps[index];
        size_t nextindex = index + offset;

        if (offset >= 3) jumps[index]--;
        else jumps[index]++;

        steps++;
        index = nextindex;
    }

    std::cout << steps << std::endl;
}
