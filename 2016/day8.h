#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

void day8()
{
	std::fstream fs("input.txt", std::ios::in);

	std::string display[6];

	for (int i = 0; i < 6; i++)
	{
		display[i] = std::string(50, '.');
	}

	std::string row;
	while (std::getline(fs, row))
	{
		std::stringstream ss(row);
		std::string tmp;

		if (row.find("rect") != std::string::npos)
		{
			ss >> tmp;
			ss.get();

			int a, b;
			ss >> a;
			ss.get();
			ss >> b;

			for (int i = 0; i < b; i++)
			{
				for (int j = 0; j < a; j++)
				{
					display[i][j] = '#';
				}
			}
		}
		else if (row.find("rotate row") != std::string::npos)
		{
			row = row.substr(13);

			int rowIndex, offset;
			ss = std::stringstream(row);
			ss >> rowIndex;
			ss.get();
			ss.get();
			ss.get();
			ss.get();
			ss >> offset;

			offset = offset % 50;

			std::vector<char> tmp(50, '.');

			for (int i = 0; i < 50; i++)
			{
				tmp[(i + offset) % 50] = display[rowIndex][i];
			}

			for (int i = 0; i < 50; i++)
			{
				display[rowIndex][i] = tmp[i];
			}
		}
		else if (row.find("rotate column") != std::string::npos)
		{
			row = row.substr(16);

			int columnIndex, offset;
			ss = std::stringstream(row);
			ss >> columnIndex;
			ss.get();
			ss.get();
			ss.get();
			ss.get();
			ss >> offset;

			offset = offset % 6;

			std::vector<char> tmp(6, '.');

			for (int i = 0; i < 6; i++)
			{
				tmp[(i + offset) % 6] = display[i][columnIndex];
			}

			for (int i = 0; i < 6; i++)
			{
				display[i][columnIndex] = tmp[i];
			}
		}
	}

	int lit = 0;
	for (int i = 0; i < 6; i++)
	{
		for (int j = 0; j < 50; j++)
		{
			std::cout << display[i][j];
			if (display[i][j] == '#')
			{
				lit++;
			}
		}

		std::cout << std::endl;
	}

	std::cout << lit << std::endl;
}
