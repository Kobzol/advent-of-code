#pragma once

#include <fstream>
#include <string>
#include <iostream>

#include <unordered_set>

bool containsAbba(const std::string& row, int i)
{
	if (i < row.size() - 3)
	{
		return row[i] != row[i + 1] && row[i] == row[i + 3] && row[i + 1] == row[i + 2];
	}
	else return false;
}
void add_aba(std::unordered_set<std::string>& babs, const std::string& row, int i)
{
	if (i < row.size() - 2)
	{
		if (row[i] == row[i + 2] && row[i] != row[i + 1])
		{
			std::string sub = row.substr(i, 3);
			if (sub.find('[') == std::string::npos && sub.find(']') == std::string::npos)
			{
				babs.insert(row.substr(i, 3));
			}
		}
	}
}

void day7()
{
	std::fstream fs("input.txt", std::ios::in);

	int ipCount = 0;

	int rowCount = 0;

	std::string row;
	while (std::getline(fs, row))
	{
		bool inBrackets = false;
		bool tls = false;
		std::unordered_set<std::string> abas;
		std::unordered_set<std::string> babs;

		for (size_t i = 0; i < row.size() - 2; i++)
		{
			if (row[i] == '[') inBrackets = true;
			else if (row[i] == ']') inBrackets = false;
			else
			{
				add_aba(inBrackets ? babs : abas, row, i);
			}
		}

		for (auto& aba : abas)
		{
			for (auto& bab : babs)
			{
				if (aba[0] == bab[1] && bab[0] == aba[1])
				{
					tls = true;
					break;
				}
			}

			if (tls) break;
		}

		if (tls)
		{
			ipCount++;
		}

		rowCount++;
	}

	std::cout << ipCount << std::endl;
}
