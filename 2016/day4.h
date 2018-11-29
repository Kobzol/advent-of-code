#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <unordered_map>
#include <algorithm>

struct CharCount
{
	char c;
	int count;
};

void day4()
{
	std::fstream fs("input.txt", std::ios::in);
	std::fstream outFs("output.txt", std::ios::out);

	int sum = 0;

	std::string row;
	while (std::getline(fs, row))
	{
		std::string word;
		int sectorId = 0;
		std::unordered_map<char, int> charMap;
		bool checkHash = false;
		std::string hash;
		std::string sentence;

		for (size_t i = 0; i < row.size() - 1; i++)
		{
			if (row[i] == '[')
			{
				checkHash = true;
			}
			else if (checkHash)
			{
				hash += row[i];
			}
			else if (isdigit(row[i]))
			{
				sectorId *= 10;
				sectorId += row[i] - '0';
			}
			else if (row[i] != '-')
			{
				if (!charMap.count(row[i]))
				{
					charMap.insert({ row[i], 0 });
				}

				charMap[row[i]]++;
				sentence += row[i];
			}
			else sentence += ' ';
		}

		std::vector<CharCount> counts;

		for (auto& entry : charMap)
		{
			counts.push_back({entry.first, entry.second});
		}

		std::sort(counts.begin(), counts.end(), [](CharCount& c1, CharCount& c2) -> bool {
			if (c1.count > c2.count) return true;
			if (c1.count < c2.count) return false;
			else return c1.c <= c2.c;
		});

		std::string computedHash;
		for (int i = 0; i < 5; i++)
		{
			computedHash += counts[i].c ;
		}

		if (computedHash == hash)
		{
			sum += sectorId;
		}

		for (int i = 0; i < sentence.size(); i++)
		{
			if (sentence[i] != ' ')
			{
				sentence[i] = (((sentence[i] - 'a') + sectorId) % 26) + 'a';
			}
		}

		outFs << sentence << " " << sectorId << std::endl;
	}

	std::cout << sum << std::endl;
}