#pragma once

#include <iostream>

void day15()
{
	const int size = 7;
	int discs[size] = {
		7, 13, 3, 5, 17, 19, 11
	};
	int starts[size] = {
		0, 0, 2, 2, 0, 7, 0
	};
	/*const int size = 2;
	int discs[size] = {
		5, 2
	};
	int starts[size] = {
		4, 1
	};*/

	int step = 0;
	while (true)
	{
		bool valid = true;
		for (int i = 0; i < size; i++)
		{
			if ((starts[i] + step + i) % discs[i] != 0)
			{
				valid = false;
				break;
			}
		}

		if (valid)
		{
			std::cout << step - 1 << std::endl;
			break;
		}

		step++;
	}
}