#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>

static int findMax(const std::vector<size_t>& memory)
{
    size_t maxIndex = 0;
    for (int i = 1; i < memory.size(); i++)
    {
        if (memory[i] > memory[maxIndex]) maxIndex = i;
    }
    return maxIndex;
}
static std::string hash(const std::vector<size_t>& memory)
{
    std::stringstream ss;
    for (auto& m : memory)
    {
        ss << m << "|";
    }
    return ss.str();
}

void day6()
{
    std::vector<size_t> memory = {
            14, 0, 15, 12, 11, 11, 3, 5, 1, 6, 8, 4, 9, 1, 8, 4
    };

    size_t steps = 0;
    std::unordered_set<std::string> visited;
    std::string repeatHash;
    while (true)
    {
        auto h = hash(memory);
        if (visited.find(h) != visited.end())
        {
            repeatHash = h;
            break;
        }
        visited.insert(h);

        size_t max = findMax(memory);
        size_t value = memory[max];
        memory[max] = 0;

        max = (max + 1) % memory.size();
        for (int i = 0; i < value; i++)
        {
            memory[max]++;
            max = (max + 1) % memory.size();
        }

        steps++;
    }

    steps = 0;
    while (true)
    {
        size_t max = findMax(memory);
        size_t value = memory[max];
        memory[max] = 0;

        max = (max + 1) % memory.size();
        for (int i = 0; i < value; i++)
        {
            memory[max]++;
            max = (max + 1) % memory.size();
        }

        steps++;

        auto h = hash(memory);
        if (h == repeatHash) break;
    }

    std::cout << steps << std::endl;
}
