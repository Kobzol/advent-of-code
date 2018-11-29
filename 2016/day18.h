#pragma once

#include <iostream>
#include <string>

bool isSafe(const std::string& row, int position)
{
	if (position < 0 || position >= row.size()) return true;
	return row[position] == '.';
}

void day18()
{
	std::string input = "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^";
	//std::string input = ".^^.^.^^^^";
	const int iterationCount = 400000;

	std::vector<std::string> map = { input };

	for (int i = 0; i < iterationCount - 1; i++)
	{
		map.push_back(std::string(map[i].size(), '.'));

		for (int j = 0; j < map[i].size(); j++)
		{
			char left = !isSafe(map[i], j - 1);
			char center = !isSafe(map[i], j);
			char right = !isSafe(map[i], j + 1);

			bool trap = false;
			if (left && center && !right) trap = true;
			if (center && right && !left) trap = true;
			if (left && !center && !right) trap = true;
			if (right && !center && !left) trap = true;

			if (trap)
			{
				map[i + 1][j] = '^';
			}
			else map[i + 1][j] = '.';
		}
	}

	int count = 0;
	for (int i = 0; i < map.size(); i++)
	{
		for (int j = 0; j < map[i].size(); j++)
		{
			if (map[i][j] == '.') count++;
		}
	}

	std::cout << count << std::endl;
}