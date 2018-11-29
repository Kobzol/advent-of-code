#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>

static std::string hash(const std::string& str)
{
    std::vector<size_t> bitmap(256, 0);
    for (auto& c : str)
    {
        bitmap[(int) c]++;
    }

    std::string hash;
    for (auto& c: bitmap)
    {
        hash += std::to_string(c) + "|";
    }

    return hash;
}

void day4()
{
    std::fstream input("input.txt");
    std::string line;
    size_t validCount = 0;

    while (std::getline(input, line))
    {
        std::stringstream ss(line);
        std::unordered_set<std::string> set;
        std::string word;

        bool valid = true;
        while (ss >> word)
        {
            if (set.find(hash(word)) != set.end())
            {
                valid = false;
                break;
            }
            set.insert({ hash(word) });
        }
        if (valid) validCount++;
    }

    std::cout << validCount << std::endl;
}
