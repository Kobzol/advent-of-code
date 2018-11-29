#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <regex>

class Instruction
{
public:
	std::string type;
	std::vector<std::string> arguments;
};

void day23()
{
	std::fstream fs("input.txt", std::ios::in);

	const std::regex cpy("cpy ((?:-?\\d+)|(?:[a-z])) ([a-z])");
	const std::regex incReg("inc ([a-z])");
	const std::regex decReg("dec ([a-z])");
	const std::regex jnz("jnz ((?:-?\\d+)|(?:[a-z])) ((?:-?\\d+)|(?:[a-z]))");
	const std::regex tgl("tgl ((?:-?\\d+)|(?:[a-z]))");

	std::vector<Instruction> instructions;
	std::string row;
	while (std::getline(fs, row))
	{
		std::smatch match;
		Instruction instruction;

		if (std::regex_search(row, match, cpy))
		{
			instruction = Instruction{ "cpy", { match[1].str(), match[2].str() } };
		}
		else if (std::regex_search(row, match, incReg))
		{
			instruction = Instruction{ "inc", { match[1].str() } };
		}
		else if (std::regex_search(row, match, decReg))
		{
			instruction = Instruction{ "dec", { match[1].str() } };
		}
		else if (std::regex_search(row, match, jnz))
		{
			instruction = Instruction{ "jnz", { match[1].str(), match[2].str() } };
		}
		else if (std::regex_search(row, match, tgl))
		{
			instruction = Instruction{ "tgl", { match[1].str() } };
		}
		else
		{
			std::cout << "error" << std::endl;
		}

		instructions.push_back(instruction);
	}

	int regs[4] = { 12, 0, 0, 0 };

	int ip = 0;
	while (ip < instructions.size())
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
				continue;
			}
		}
		else if (inst.type == "tgl")
		{
			int target = isalpha(inst.arguments[0][0]) ? regs[inst.arguments[0][0] - 'a'] : std::stoi(inst.arguments[0]);
			target += ip;

			if (target < 0 || target >= instructions.size())
			{
				ip++;
				continue;
			}

			if (instructions[target].arguments.size() == 1)
			{
				if (instructions[target].type == "inc") instructions[target].type = "dec";
				else instructions[target].type = "inc";
			}
			else
			{
				if (instructions[target].type == "jnz") instructions[target].type = "cpy";
				else instructions[target].type = "jnz";
			}
		}

		ip++;
	}

	std::cout << regs[0] << std::endl;
}
