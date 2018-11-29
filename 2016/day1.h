#pragma once

#include <fstream>
#include <string>
#include <unordered_set>
#include <iostream>

int rotateRight(int dir)
{
	return (dir + 1) % 4;
}
int rotateLeft(int dir)
{
	return ((dir - 1) + 4) % 4;
}
std::string posToStr(int* pos)
{
	return std::to_string(pos[0]) + "#" + std::to_string(pos[1]);
}

void day1()
{
	std::fstream fs("input.txt", std::ios::in);

	int dirs[4][2] = {
		{1, 0},
		{0, 1},
		{-1, 0},
		{0, -1}
	};
	int dir = 0;
	int pos[2] = { 0, 0 };

	std::unordered_set<std::string> positions;

	std::string command;
	while (fs >> command)
	{
		if (command[command.size() - 1] == ',')
		{
			command = command.substr(0, command.size() - 1);
		}
		char dirChange = command[0];
		int count = std::stoi(command.substr(1));

		dir = dirChange == 'R' ? rotateRight(dir) : rotateLeft(dir);

		for (int i = 0; i < count; i++)
		{
			positions.insert({ posToStr(pos) });

			pos[0] += dirs[dir][0];
			pos[1] += dirs[dir][1];

			if (positions.count(posToStr(pos)))
			{
				std::cout << abs(pos[0]) + abs(pos[1]) << std::endl;
			}
		}
	}
}