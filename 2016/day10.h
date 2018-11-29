#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <cassert>

struct BotInit
{
	int bot, value;
};
struct BotRule
{
	int lowTarget, highTarget;
	bool lowBot, highBot;
};
struct Bot
{
	int id;
	std::vector<int> values;
	std::vector<BotRule> rules;
};

void executeBot(Bot& bot, std::unordered_map<int, Bot>& bots, std::unordered_map<int, int>& outputs)
{
	if (bot.values.size() < 2)
	{
		return;
	}

	int min = 0, max = 0;
	for (size_t i = 1; i < bot.values.size(); i++)
	{
		if (bot.values[i] < bot.values[min]) min = i;
		if (bot.values[i] > bot.values[max]) max = i;
	}

	if (bot.values[min] == 17 && bot.values[max] == 61)
	{
		std::cout << bot.id << std::endl;
	}

	int minValue = bot.values[min];
	int maxValue = bot.values[max];

	if (bot.rules[0].lowBot)
	{
		bots[bot.rules[0].lowTarget].values.push_back(minValue);
		executeBot(bots[bot.rules[0].lowTarget], bots, outputs);
	}
	else
	{
		assert(!outputs.count(bot.rules[0].lowTarget));
		outputs[bot.rules[0].lowTarget] = minValue;
	}

	if (bot.rules[0].highBot)
	{
		bots[bot.rules[0].highTarget].values.push_back(maxValue);
		executeBot(bots[bot.rules[0].highTarget], bots, outputs);
	}
	else
	{
		assert(!outputs.count(bot.rules[0].highTarget));
		outputs[bot.rules[0].highTarget] = maxValue;
	}
}

void day10()
{
	std::fstream fs("input.txt", std::ios::in);

	std::vector<BotInit> botInits;
	std::unordered_map<int, Bot> bots;
	std::unordered_map<int, int> outputs;

	std::string row;
	while (std::getline(fs, row))
	{
		if (row[0] == 'v')
		{
			row = row.substr(6);
			int value = 0;
			int index = 0;
			while (isdigit(row[index]))
			{
				value *= 10;
				value += row[index] - '0';
				index++;
			}

			row = row.substr(index + 13);
			int bot;
			std::stringstream ss(row);
			ss >> bot;

			botInits.push_back(BotInit{ bot, value });
		}
		else
		{
			row = row.substr(4);
			std::stringstream ss(row);
			int bot;
			ss >> bot;

			int lowValue, highValue;
			bool lowBot = true, highBot = true;

			row = row.substr(row.find("low to") + 7);
			if (row[0] != 'b')
			{
				lowBot = false;
			}

			row = row.substr(row.find(" ") + 1);
			ss = std::stringstream(row);
			ss >> lowValue;

			row = row.substr(row.find("high to") + 8);
			if (row[0] != 'b')
			{
				highBot = false;
			}

			row = row.substr(row.find(" ") + 1);
			ss = std::stringstream(row);
			ss >> highValue;

			if (!bots.count(bot))
			{
				bots.insert({ bot, Bot{bot} });
			}

			bots[bot].rules.push_back(BotRule{ lowValue, highValue, lowBot, highBot });
		}
	}

	for (auto& bot : bots)
	{
		assert(bot.second.rules.size() < 2);
	}

	for (size_t i = 0; i < botInits.size(); i++)
	{
		BotInit bi = botInits[i];
		bots[bi.bot].values.push_back(bi.value);

		executeBot(bots[bi.bot], bots, outputs);
	}

	std::cout << outputs[0] * outputs[1] * outputs[2] << std::endl;
}