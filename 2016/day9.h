#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <sstream>

typedef unsigned long long ulong;

ulong decompress(const std::string& row, int index, int length)
{
	if (index >= row.size()) return 0;
	if (length < 1) return 0;

	if (isspace(row[index]))
	{
		return decompress(row, index + 1, length - 1);
	}
	if (row[index] == '(')
	{
		std::string from = row.substr(index + 1);
		std::stringstream ss(from);
		int charCount, repeatCount;
		ss >> charCount;
		ss.get();
		ss >> repeatCount;

		int indexAdd = from.find(')') + 2;

		ulong innerCount = repeatCount * decompress(row, index + indexAdd, charCount);

		return innerCount + decompress(row, index + indexAdd + charCount, length - charCount - indexAdd);
	}
	else
	{
		int count = 0;
		int indexAdd = 0;
		while (indexAdd < length && (index + indexAdd) < row.size() && row[(index + indexAdd)] != '(')
		{
			if (!isspace(row[(index + indexAdd)]))
			{
				count++;
			}
			indexAdd++;
		}

		return count + decompress(row, index + indexAdd, length - indexAdd);
	}
}

void day9()
{
	std::fstream fs("input.txt", std::ios::in);

	ulong count = 0;

	std::string row;
	while (std::getline(fs, row))
	{
		count = decompress(row, 0, row.size());

		/*for (size_t i = 0; i < row.size(); i++)
		{
			if (isspace(row[i]))
			{
				continue;
			}
			else if (row[i] == '(')
			{
				std::string from = row.substr(i + 1);
				std::stringstream ss(from);
				int charCount, repeatCount;
				ss >> charCount;
				ss.get();
				ss >> repeatCount;

				i += from.find(')') + 2;

				std::string sub = row.substr(i, charCount);

				i += charCount - 1;

				for (int j = 0; j < repeatCount; j++)
				{
					decompressed += sub;
				}
			}
			else decompressed += row[i];
		}*/
	}

	std::cout << count << std::endl;
}