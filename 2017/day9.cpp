#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>

static bool isGarbage(const std::vector<char>& stack)
{
    return !stack.empty() && stack.back() == '<';
}

void day9()
{
    std::fstream input("input.txt");
    std::string line;

    while (std::getline(input, line))
    {
        std::vector<char> stack;
        size_t score = 0;
        bool ignore = false;
        for (int i = 0; i < line.size(); i++)
        {
            char c = line[i];
            if (ignore)
            {
                ignore = false;
            }
            else if (line[i] == '!')
            {
                ignore = true;
            }
            else if (isGarbage(stack) && c == '>')
            {
                stack.pop_back();
            }
            else if (!isGarbage(stack) && c == '<')
            {
                stack.push_back(c);
            }
            else if (!isGarbage(stack) && c == '{')
            {
                stack.push_back(c);
            }
            else if (!isGarbage(stack) && c == '}')
            {
                stack.pop_back();
            }
            else if (isGarbage(stack))
            {
                score++;
            }
        }

        std::cout << score << std::endl;
    }
}
