#pragma once

#include "day23.h"

#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <regex>

std::string simulate(std::vector<Instruction>& instructions, int steps, int* regs)
{
	std::string output;

	int ip = 0;
	int stepsRan = 0;
	while (ip < instructions.size() && stepsRan < steps)
	{
		Instruction& inst = instructions[ip];

		if (inst.type == "cpy")
		{
			if (isalpha(inst.arguments[1][0]))
			{
				int source = isalpha(inst.arguments[0][0]) ? regs[inst.arguments[0][0] - 'a'] : std::stoi(inst.arguments[0]);
				int target = inst.arguments[1][0] - 'a';
				regs[target] = source;
			}
		}
		else if (inst.type == "inc" || inst.type == "dec")
		{
			if (isalpha(inst.arguments[0][0]))
			{
				int target = inst.arguments[0][0] - 'a';
				regs[target] += inst.type == "inc" ? 1 : -1;
			}
		}
		else if (inst.type == "jnz")
		{
			int condition = isalpha(inst.arguments[0][0]) ? regs[inst.arguments[0][0] - 'a'] : std::stoi(inst.arguments[0]);
			int target = isalpha(inst.arguments[1][0]) ? regs[inst.arguments[1][0] - 'a'] : std::stoi(inst.arguments[1]);

			if (condition != 0)
			{
				ip += target;
				stepsRan++;
				continue;
			}
		}
		else if (inst.type == "out")
		{
			int targetNum = isalpha(inst.arguments[0][0]) ? regs[inst.arguments[0][0] - 'a'] : std::stoi(inst.arguments[0]);
			if (targetNum < 0 || targetNum > 1) return "error";

			char target = targetNum + '0';

			if (output.size() == 0 && target != '0') return "error";
			if (output.size() > 0 && output[output.size() - 1] == target) return "error";
			output.push_back(target);
		}

		ip++;
		stepsRan++;
	}

	return output;
}

void day25()
{
	std::fstream fs("input.txt", std::ios::in);

	const std::regex cpy("cpy ((?:-?\\d+)|(?:[a-z])) ([a-z])");
	const std::regex incReg("inc ([a-z])");
	const std::regex decReg("dec ([a-z])");
	const std::regex jnz("jnz ((?:-?\\d+)|(?:[a-z])) ((?:-?\\d+)|(?:[a-z]))");
	const std::regex out("out ((?:-?\\d+)|(?:[a-z]))");

	std::vector<Instruction> instructions;
	std::string row;
	while (std::getline(fs, row))
	{
		std::smatch match;
		Instruction instruction;

		if (std::regex_search(row, match, cpy))
		{
			instruction = Instruction{ "cpy",{ match[1].str(), match[2].str() } };
		}
		else if (std::regex_search(row, match, incReg))
		{
			instruction = Instruction{ "inc",{ match[1].str() } };
		}
		else if (std::regex_search(row, match, decReg))
		{
			instruction = Instruction{ "dec",{ match[1].str() } };
		}
		else if (std::regex_search(row, match, jnz))
		{
			instruction = Instruction{ "jnz",{ match[1].str(), match[2].str() } };
		}
		else if (std::regex_search(row, match, out))
		{
			instruction = Instruction{ "out",{ match[1].str() } };
		}
		else
		{
			std::cout << "error" << std::endl;
		}

		instructions.push_back(instruction);
	}

	int a = 0;
	while (true)
	{
		int regs[4] = { a, 0, 0, 0 };
		std::string output = simulate(instructions, 1000000, regs);

		if (output != "error")
		{
			std::cout << a << std::endl;
			std::cout << "Length: " << output.size() << std::endl;
		}

		a++;
	}
}