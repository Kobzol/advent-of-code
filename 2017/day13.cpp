#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>
#include <cassert>

static int getPosition(int range, int iteration)
{
    int skip = (range - 1) * 2;
    int left = iteration % skip;
    if (left == 0) return 0;

    int pos = 0;
    for (int i = 0; i < range - 1; i++)
    {
        pos++;
        left--;
        if (left == 0) return pos;
    }

    for (int i = 0; i < range - 1; i++)
    {
        pos--;
        left--;
        if (left == 0) return pos;
    }

    return pos;
}
static int getScore(int delay, int maximum, std::unordered_map<int, int>& scanners)
{
    int score = 0;
    for (int i = 0; i <= maximum; i++)
    {
        if (scanners.find(i) == scanners.end()) continue;
        int pos = getPosition(scanners[i], i + delay);
        assert(pos >= 0 && pos < scanners[i]);

        if (pos == 0)
        {
            score += i * scanners[i] + 1;
        }
    }

    return score;
}

void day13()
{
    std::fstream input("input.txt");
    std::string line;

    std::unordered_map<int, int> scanners;
    int maximum = 0;
    while (std::getline(input, line))
    {
        int num = 0;
        int i = 0;
        while (isdigit(line[i]))
        {
            num *= 10;
            num += line[i] - '0';
            i++;
        }
        i += 2;

        maximum = std::max(maximum, num);
        int range = 0;
        while (i < line.size() && isdigit(line[i]))
        {
            range *= 10;
            range += line[i] - '0';
            i++;
        }

        scanners.insert({ num, range });
    }

    int delay = 0;
    while (true)
    {
        if (getScore(delay++, maximum, scanners) == 0) break;
    }

    std::cout << delay - 1 << std::endl;
}
