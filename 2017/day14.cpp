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

std::vector<unsigned int> knotHash(const std::string& input);

static size_t findRegions(size_t bitmap[128][128], int i, int j)
{
    if (i < 0 || i >= 128 || j < 0 || j >= 128) return 0;

    size_t value = bitmap[i][j];
    if (value == 2) return 0;
    bitmap[i][j] = 2;
    if (value == 0) return 0;

    value += findRegions(bitmap, i + 1, j);
    value += findRegions(bitmap, i - 1, j);
    value += findRegions(bitmap, i, j + 1);
    value += findRegions(bitmap, i, j - 1);
    return value;
}

void day14()
{
    size_t bitmap[128][128] = {};
    size_t size = 8;
    for (int i = 0; i < 128; i++)
    {
        std::string input = "stpzcrnm-" + std::to_string(i);
        auto hash = knotHash(input);
        for (int j = 0; j < 128; j++)
        {
            bitmap[i][j] = (hash[j / size] & (1 << (7 - (j % size)))) > 0 ? 1 : 0;
        }
    }

    int regions = 0;
    for (int i = 0; i < 128; i++)
    {
        for (int j = 0; j < 128; j++)
        {
            regions += findRegions(bitmap, i, j) > 0 ? 1 : 0;
        }
    }

    std::cout << regions << std::endl;
}
