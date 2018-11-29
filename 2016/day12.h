#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <regex>

void day12()
{
	std::fstream fs("input.txt", std::ios::in);

	const std::regex valToReg("cpy (-?\\d+) ([a-z])");
	const std::regex regToReg("cpy ([a-z]) ([a-z])");
	const std::regex incReg("inc ([a-z])");
	const std::regex decReg("dec ([a-z])");
	const std::regex jnz("jnz ([a-z]) (-?\\d+)");
	const std::regex jnzVal("jnz (-?\\d+) (-?\\d+)");

	int regs[4] = { 0, 0, 1, 0 };

	std::vector<std::string> instructions;

	std::string row;
	while (std::getline(fs, row))
	{
		instructions.push_back(row);
	}

	int instruction = 0;
	while (instruction < instructions.size())
	{
		std::smatch match;
		std::string row = instructions[instruction];

		if (std::regex_search(row, match, valToReg))
		{
			regs[match[2].str()[0] - 'a'] = std::stoi(match[1].str());
		}
		else if (std::regex_search(row, match, regToReg))
		{
			regs[match[2].str()[0] - 'a'] = regs[match[1].str()[0] - 'a'];
		}
		else if (std::regex_search(row, match, incReg))
		{
			regs[match[1].str()[0] - 'a']++;
		}
		else if (std::regex_search(row, match, decReg))
		{
			regs[match[1].str()[0] - 'a']--;
		}
		else if (std::regex_search(row, match, jnz))
		{
			int value = regs[match[1].str()[0] - 'a'];
			if (value != 0)
			{
				instruction += std::stoi(match[2].str());
				continue;
			}
		}
		else if (std::regex_search(row, match, jnzVal))
		{
			int value = std::stoi(match[1].str());
			if (value != 0)
			{
				instruction += std::stoi(match[2].str());
				continue;
			}
		}
		else
		{
			std::cout << "error" << std::endl;
		}

		instruction++;
	}

	std::cout << regs[0] << std::endl;
}