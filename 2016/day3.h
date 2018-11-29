#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

void day3()
{
	std::fstream fs("input.txt", std::ios::in);
	
	int valid = 0;
	int rowCount = 0;

	int pos[3][3];

	std::string row;
	while (std::getline(fs, row))
	{
		std::stringstream ss(row);

		ss >> pos[0][rowCount] >> pos[1][rowCount] >> pos[2][rowCount];
		rowCount++;

		if (rowCount == 3)
		{
			for (int i = 0; i < 3; i++)
			{
				if (pos[i][0] + pos[i][1] > pos[i][2] &&
					pos[i][0] + pos[i][2] > pos[i][1] &&
					pos[i][1] + pos[i][2] > pos[i][0])
				{
					valid++;
				}
			}

			rowCount = 0;
		}
	}

	std::cout << valid << std::endl;
}