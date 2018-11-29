#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

static size_t getDivisibleSum(const std::vector<size_t>& numbers)
{
    for (int i = 0; i < numbers.size(); i++)
    {
        for (int j = i + 1; j < numbers.size(); j++)
        {
            if (numbers[i] % numbers[j] == 0) return numbers[i] / numbers[j];
            if (numbers[j] % numbers[i] == 0) return numbers[j] / numbers[i];
        }
    }

    return 0;
}

void day2()
{
    std::ifstream fs("input.txt");
    std::string line;
    size_t checksum = 0;

    while (std::getline(fs, line))
    {
        std::stringstream ss(line);
        std::vector<size_t> numbers;
        size_t num;
        while (ss >> num)
        {
            numbers.push_back(num);
        }

        checksum += getDivisibleSum(numbers);
    }

    std::cout << checksum << std::endl;
}
