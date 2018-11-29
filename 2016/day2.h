#pragma once

#include <fstream>
#include <string>
#include <unordered_map>

void day2()
{
	std::fstream fs("input.txt", std::ios::in);

	int pos[2] = { 2, 0 };
	std::unordered_map<char, std::vector<int>> dirs = {
		{'U', {-1, 0}},
		{'R', {0, 1}},
		{'D', {1, 0}},
		{'L', {0, -1}}
	};

	std::string map[5] = {
		{"  1  "},
		{" 234 "},
		{"56789"},
		{" ABC "},
		{"  D  "}
	};

	std::string row;
	while (fs >> row)
	{
		for (int i = 0; i < row.size(); i++)
		{
			char dir = row[i];
			std::vector<int> offset = dirs[dir];
			int nextPos[2] = {
				pos[0] + offset[0],
				pos[1] + offset[1]
			};
			if (nextPos[0] >= 0 && nextPos[0] < 5 && nextPos[1] >= 0 && nextPos[1] < 5 && map[nextPos[0]][nextPos[1]] != ' ')
			{
				pos[0] = nextPos[0];
				pos[1] = nextPos[1];
			}
		}

		std::cout << map[pos[0]][pos[1]];
	}

	std::cout << std::endl;
}