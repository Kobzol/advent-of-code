#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

using Grid = std::vector<std::string>;
using Replacement = std::pair<Grid, Grid>;

static Grid flip(Grid grid, bool horizontal)
{
    Grid othergrid = grid;

    if (horizontal)
    {
        for (int i = 0; i < othergrid.size(); i++)
        {
            for (int j = 0; j < othergrid.size(); j++)
            {
                othergrid[i][j] = grid[i][grid.size() - j - 1];
            }
        }
    }
    else
    {
        for (int i = 0; i < othergrid.size(); i++)
        {
            othergrid[i] = grid[grid.size() - i - 1];
        }
    }

    return othergrid;
}
static Grid rotate(Grid grid, int count)
{
    Grid result = grid;
    Grid tmp;

    for (int c = 0; c < count; c++)
    {
        tmp = result;
        for (int x = 0; x < grid.size(); x++)
        {
            for (int y = 0; y < grid.size(); y++)
            {
                result[y][grid.size() - x - 1] = tmp[x][y];
            }
        }
    }

    return result;
}

static bool matchesReplacement(Grid& grid, size_t x, size_t y, Grid replacement, bool test = false)
{
    if (!test)
    {
        for (int i = 0; i < replacement.size(); i++)
        {
            for (int j = 0; j < replacement.size(); j++)
            {
                if (grid[x + i][y + j] != replacement[i][j]) return false;
            }
        }
        return true;
    }
    else
    {
        std::vector<Grid> grids = {
                replacement,
                flip(replacement, true),
                flip(replacement, false),
                flip(flip(replacement, true), false),
                rotate(replacement, 1),
                flip(rotate(replacement, 1), true),
                flip(rotate(replacement, 1), false),
                flip(flip(rotate(replacement, 1), true), false),
                rotate(replacement, 2),
                flip(rotate(replacement, 2), true),
                flip(rotate(replacement, 2), false),
                flip(flip(rotate(replacement, 2), true), false),
                rotate(replacement, 3),
                flip(rotate(replacement, 3), true),
                flip(rotate(replacement, 3), false),
                flip(flip(rotate(replacement, 3), true), false)
        };

        for (auto& rep: grids)
        {
            if (matchesReplacement(grid, x, y, rep)) return true;
        }

        return false;
    }
}
static void printGrid(const Grid& grid)
{
    for (auto& row: grid)
    {
        for (auto c: row)
        {
            std::cout << c << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void day21()
{
    std::fstream input("input.txt");
    std::string line;

    std::vector<Replacement> replacements;
    while (std::getline(input, line))
    {
        auto first = line.substr(0, line.find(" => ")) + '/';
        auto second = line.substr(line.find(" => ") + 4) + '/';

        Replacement replacement({}, {});
        while (first.find('/') != std::string::npos)
        {
            auto row = first.substr(0, first.find('/'));
            replacement.first.push_back(row);
            first = first.substr(first.find('/') + 1);
        }
        while (second.find('/') != std::string::npos)
        {
            auto row = second.substr(0, second.find('/'));
            replacement.second.push_back(row);
            second = second.substr(second.find('/') + 1);
        }

        replacements.push_back(replacement);
    }

    Grid grid = {
            ".#.",
            "..#",
            "###"
    };
    for (int i = 0; i < 18; i++)
    {
        size_t width = grid.size() % 2 == 0 ? 2 : 3;
        size_t nextDim = width + 1;
        size_t newWidth = (grid.size() / width) * nextDim;

        Grid newGrid;
        for (size_t j = 0; j < newWidth; j++)
        {
            std::string str(newWidth, '.');
            newGrid.push_back(str);
        }

        for (size_t  x = 0; x < grid.size(); x += width)
        {
            for (size_t  y = 0; y < grid.size(); y += width)
            {
                for (auto& rep: replacements)
                {
                    if (rep.first.size() == width && matchesReplacement(grid, x, y, rep.first, true))
                    {
                        size_t xstart = (x / width) * nextDim;
                        size_t ystart = (y / width) * nextDim;
                        for (size_t xi = 0; xi < nextDim; xi++)
                        {
                            for (size_t yi = 0; yi < nextDim; yi++)
                            {
								newGrid[xstart + xi][ystart + yi] = rep.second[xi][yi];
                            }
                        }
						break;
                    }
                }
            }
        }

		grid = newGrid;
    }

    int count = 0;
    for (auto& row: grid)
    {
        for (auto& c: row)
        {
            if (c == '#') count++;
        }
    }

    std::cout << count << std::endl;
}
