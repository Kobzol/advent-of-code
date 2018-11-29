#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

static void reverse(std::vector<int>& numbers, int position, int length)
{
    int end = (position + length) % numbers.size();
    for (int i = 0; i < length / 2; i++)
    {
        std::swap(numbers[(position + i) % numbers.size()],
                  numbers[((end - 1 - i) + numbers.size()) % numbers.size()]);
    }
}

std::vector<unsigned int> knotHash(const std::string& input)
{
	std::vector<int> lengths;

	for (auto c : input)
	{
		lengths.push_back(c);
	}

	lengths.push_back(17);
	lengths.push_back(31);
	lengths.push_back(73);
	lengths.push_back(47);
	lengths.push_back(23);

    size_t position = 0;
    size_t skip = 0;
    std::vector<int> numbers;
    for (int i = 0; i < 256; i++) numbers.push_back(i);

	for (int j = 0; j < 64; j++)
	{
		for (int i = 0; i < lengths.size(); i++)
		{
			reverse(numbers, position, lengths[i]);
			position += lengths[i] + skip;
			skip++;
		}
	}

	std::vector<unsigned int> sparsehash;
	for (int i = 0; i < numbers.size() / 16; i++)
	{
		unsigned int xor = numbers[i * 16];
		for (int j = 1; j < 16; j++)
		{
			xor ^= (unsigned int) numbers[(i * 16) + j];
		}
		sparsehash.push_back(xor);
	}

    return sparsehash;
}

void day10()
{
	size_t position = 0;
	size_t skip = 0;
	std::vector<int> numbers;
	for (int i = 0; i < 256; i++) numbers.push_back(i);

	std::string input = "120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113";
	std::vector<int> lengths;

	for (auto c : input)
	{
		lengths.push_back((int)c);
	}

	lengths.push_back(17);
	lengths.push_back(31);
	lengths.push_back(73);
	lengths.push_back(47);
	lengths.push_back(23);

	for (int j = 0; j < 64; j++)
	{
		for (int i = 0; i < lengths.size(); i++)
		{
			reverse(numbers, position, lengths[i]);
			position += lengths[i] + skip;
			skip++;
		}
	}

	std::vector<unsigned int> sparsehash;
	for (int i = 0; i < numbers.size() / 16; i++)
	{
		unsigned int xor = numbers[i * 16];
		for (int j = 1; j < 16; j++)
		{
			xor ^= (unsigned int) numbers[(i * 16) + j];
		}
		sparsehash.push_back(xor);
	}

	for (auto& hash : sparsehash)
	{
		std::cout << std::setfill('0') << std::setw(2) << std::hex << hash;
	}
    
	getchar();
}
