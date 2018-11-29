#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

static size_t add(std::vector<size_t>& data, std::initializer_list<int> indices)
{
	size_t index = 0;
	for (auto ind : indices)
	{
		index += data[ind >= 0 ? (ind) : (data.size() + ind)];
	}

	return index;
}

void day3()
{
    size_t input = 277678;
    int diameter = 5;
    size_t index = 0;
	int inner = 1;

    std::vector<size_t> data = { 1, 1, 2, 4, 5, 10, 11, 23, 25 };
	while (index < input)
	{
		for (int j = 0; j < 4; j++)
		{
			// corner
			index = add(data, { -1, inner });
			data.push_back(index);

			// row/column
			int end = j == 0 ? diameter - 3 : diameter - 2;
			for (int i = 0; i < end; i++)
			{
				index = add(data, { -1, inner });
				if (i == 0)
				{
					index += add(data, { -2 });
				}
				else index += add(data, { inner - 1 });

				if (j == 3 && i == end - 1)
				{
					index += add(data, { inner + 1 });
				}

				if (i != end - 1)
				{
					index += add(data, { inner + 1 });
					inner++;
				}

				data.push_back(index);
			}
		}

		// overlap corner
		index = add(data, { -1, inner, inner + 1 });
		data.push_back(index);
		inner++;

        diameter += 2;
    }
}
