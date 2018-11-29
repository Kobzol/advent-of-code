#pragma once

#include <iostream>
#include <fstream>
#include <regex>
#include <string>
#include <vector>
#include <algorithm>

std::string rotate(const std::string& str, bool left, int steps)
{
	std::string copy = str;

	for (size_t i = 0; i < str.size(); i++)
	{
		int target = left ? (i - steps) : (i + steps);
		target = (target + str.size()) % str.size();
		copy[target] = str[i];
	}

	return copy;
}

void day21()
{
	std::fstream fs("input.txt", std::ios::in);

	const std::regex swapPos("swap position (\\d+) with position (\\d+)");
	const std::regex swapLetter("swap letter (\\w+) with letter (\\w+)");
	const std::regex rotateFixed("rotate (left|right) (\\d+) step(s?)");
	const std::regex rotateLetter("rotate based on position of letter (\\w+)");
	const std::regex reverse("reverse positions (\\d+) through (\\d+)");
	const std::regex move("move position (\\d+) to position (\\d+)");

	std::vector<std::string> instructions;

	std::string row;
	while (std::getline(fs, row))
	{
		instructions.push_back(row);
	}

	//std::reverse(instructions.begin(), instructions.end());

	std::string target = "fbgdceah";
	std::string input = "abcdefgh";
	do
	{
		std::string password = input;
		for (std::string& row : instructions)
		{
			std::smatch match;

			if (std::regex_match(row, match, swapPos))	// OK
			{
				std::swap(password[std::stoi(match[1].str())], password[std::stoi(match[2].str())]);
			}
			else if (std::regex_match(row, match, swapLetter))	// OK
			{
				char letters[2] = { match[1].str()[0], match[2].str()[0] };

				int first = password.find(letters[0]);
				int second = password.find(letters[1]);
				std::swap(password[first], password[second]);
			}
			else if (std::regex_match(row, match, rotateFixed))  // OK changed
			{
				bool left = match[1].str() == "left";
				int steps = std::stoi(match[2].str());

				//left = !left; // unscramble

				password = rotate(password, left, steps);
			}
			else if (std::regex_match(row, match, rotateLetter))	// TODO changed
			{
				char letter = match[1].str()[0];
				int pos = password.find(letter);
				if (pos >= 4) pos++;
				pos++;

				password = rotate(password, false, pos);	// unscramble - true
			}
			else if (std::regex_match(row, match, reverse))	// OK
			{
				int positions[2] = {
					std::stoi(match[1].str()),
					std::stoi(match[2].str()) + 1
				};

				std::string copy = password;
				std::reverse(password.begin() + positions[0], password.begin() + positions[1]);
			}
			else if (std::regex_match(row, match, move))	// OK changed
			{
				int positions[2] = {
					std::stoi(match[1].str()),
					std::stoi(match[2].str())
				};

				//std::swap(positions[0], positions[1]);	// unscramble

				char letter = password[positions[0]];
				password.erase(password.begin() + positions[0]);
				password.insert(password.begin() + positions[1], letter);
			}
		}

		if (password == target)
		{
			std::cout << input << std::endl;
			break;
		}
	} while (std::next_permutation(input.begin(), input.end()));

	std::cout << "END" << std::endl;
	//std::cout << password << std::endl;
}
