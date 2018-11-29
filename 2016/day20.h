#pragma once

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

void day20()
{
	std::fstream fs("input.txt", std::ios::in);

	std::vector<std::tuple<unsigned long long, unsigned long long>> doubles;

	std::string row;
	while (std::getline(fs, row))
	{
		std::stringstream ss(row);
		unsigned long long first, second;
		ss >> first;
		ss.get();
		ss >> second;

		if (first >= second)
		{
			std::swap(first, second);
		}

		doubles.push_back({ first, second });
	}

	std::sort(doubles.begin(), doubles.end(), [](std::tuple<unsigned long long, unsigned long long>& lhs, std::tuple<unsigned long long, unsigned long long>& rhs) -> bool {
		return std::get<0>(lhs) < std::get<0>(rhs);
	});

	unsigned long long max = 0;
	unsigned long long allowed = 0;
	for (int i = 0; i < doubles.size(); i++)
	{
		if (std::get<0>(doubles[i]) > max + 1)
		{
			allowed += (std::get<0>(doubles[i]) - max) - 1;
		}
		max = std::max(max, std::get<1>(doubles[i]));
	}

	std::cout << allowed << std::endl;
}