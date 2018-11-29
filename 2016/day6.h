#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <unordered_map>
#include <algorithm>

#include "day4.h"

void day6()
{
	std::fstream fs("input.txt", std::ios::in);

	const int width = 8;

	std::unordered_map<char, int> counts[width];

	std::string row;
	while (std::getline(fs, row))
	{
		for (size_t i = 0; i < row.size(); i++)
		{
			if (!counts[i].count(row[i]))
			{
				counts[i].insert({ row[i], 0 });
			}

			counts[i][row[i]]++;
		}
	}

	for (int i = 0; i < width; i++)
	{
		std::vector<CharCount> charCounts;
		for (auto& entry : counts[i])
		{
			charCounts.push_back(CharCount{ entry.first, entry.second });
		}

		std::sort(charCounts.begin(), charCounts.end(), [](CharCount& l, CharCount& r)
		{
			return l.count < r.count;
		});

		std::cout << charCounts[0].c;
	}

	std::cout << std::endl;
}