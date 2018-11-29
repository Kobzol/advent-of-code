#pragma once

#include <iostream>
#include <unordered_set>
#include <list>

void day19()
{
	int totalNumber = 3017957;

	std::list<int> elves;
	for (int i = 0; i < totalNumber; i++)
	{
		elves.push_back(i + 1);
	}

	std::list<int>::iterator iter = elves.begin(), delIter = elves.begin();

	for (int i = 0; i < totalNumber / 2; i++)
	{
		delIter++;
	}

	while (elves.size() > 1)
	{
		std::list<int>::iterator copied = delIter;
		
		if (delIter == elves.end()) delIter = elves.begin();
		delIter++;
		if (delIter == elves.end()) delIter = elves.begin();

		if (elves.size() % 2 != 0)
		{
			delIter++;
			if (delIter == elves.end()) delIter = elves.begin();
		}

		elves.erase(copied);

		if (iter == elves.end()) iter = elves.begin();
		iter++;
		if (iter == elves.end()) iter = elves.begin();
	}

	std::cout << *elves.begin() << std::endl;
}