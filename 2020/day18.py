results = []

OPS = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b
}


def evaluate_part1(data, index):
    last_op = None
    result = None

    def handle_value(value):
        nonlocal result, last_op
        # print(f"Handling {value} with {last_op} and {result}")
        if result is None:
            assert last_op is None
            result = value
        else:
            assert last_op is not None
            result = OPS[last_op](result, value)
            last_op = None
        # print(f"Result is {result}")

    buffer = ""

    def flush_buffer():
        nonlocal buffer
        if buffer:
            value = int(buffer)
            handle_value(value)
            buffer = ""

    while index < len(data):
        ch = data[index]
        if ch == ")":
            flush_buffer()
            return (result, index + 1)
        elif ch == "(":
            value, next_index = evaluate_part1(data, index + 1)
            index = next_index - 1
            handle_value(value)
        elif ch.isdigit():
            buffer += ch
        elif ch in ("+", "*"):
            last_op = ch
        elif ch == " ":
            flush_buffer()
        else:
            assert False
        index += 1

    flush_buffer()
    return (result, len(data))


def tokenize(data):
    num_buffer = ""

    def flush_buffer():
        nonlocal num_buffer
        if num_buffer:
            yield {
                "type": "number",
                "value": int(num_buffer)
            }
            num_buffer = ""

    for c in data:
        if c.isdigit():
            num_buffer += c
        elif c in ("+", "*"):
            yield {
                "type": "operator",
                "value": c
            }
        elif c in ("(", ")"):
            if c == ")":
                yield from flush_buffer()
            yield {
                "type": "parenthesis",
                "value": c
            }
        elif c == " ":
            yield from flush_buffer()
    yield from flush_buffer()


def shunting_yard(data):
    output_queue = []
    operator_stack = []

    for token in tokenize(data):
        type = token["type"]
        value = token["value"]
        if type == "number":
            output_queue.append(value)
        elif type == "parenthesis":
            if value == "(":
                operator_stack.append(value)
            elif value == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == "(":
                    operator_stack.pop()
        elif type == "operator":
            while operator_stack and operator_stack[-1] != "(" and operator_stack[-1] == "+":
                output_queue.append(operator_stack.pop())
            operator_stack.append(value)
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue


def eval_rpn(rpn):
    stack = []
    for item in rpn:
        if isinstance(item, int):
            stack.append(item)
        else:
            stack.append(OPS[item](stack.pop(), stack.pop()))
    assert len(stack) == 1
    return stack[0]


with open("input.txt") as f:
    for line in f:
        line = line.strip()
        rpn = shunting_yard(line)
        result = eval_rpn(rpn)
        # print(result, end, len(line))
        # assert end == len(line)
        results.append(result)

print(sum(results))
