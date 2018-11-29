#pragma once

#include <iostream>
#include <string>

void day16()
{
	int size = 35651584;
	std::string input = "01111001100111011";

	while (input.size() < size)
	{
		std::string copy = input;
		std::reverse(copy.begin(), copy.end());

		for (int i = 0; i < copy.size(); i++)
		{
			if (copy[i] == '0') copy[i] = '1';
			else copy[i] = '0';
		}

		input = input + "0" + copy;
	}

	input = input.substr(0, size);

	while (input.size() % 2 == 0)
	{
		std::string checksum;
		for (int i = 0; i < input.size() - 1; i += 2)
		{
			if (input[i] == input[i + 1])
			{
				checksum += "1";
			}
			else checksum += "0";
		}

		input = checksum;
	}

	std::cout << input << std::endl;
}