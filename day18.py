class SnailNumber:
    def __init__(self, initial):
        if "," in initial or "[" in initial:
            #print("Type pair")
            self.type = "pair"
            list_depth = 0
            for char_id, char in enumerate(initial):
                #print(f"{char_id}: {char} at {list_depth}")
                if char == "[":
                    list_depth += 1
                elif char == "]":
                    list_depth -= 1
                elif list_depth == 1 and char == ",":
                    #print(f"Creating left with {initial[1:char_id]}")
                    self.left = SnailNumber(initial[1:char_id])
                    #print(f"Creating right with {initial[char_id + 1:-1]}")
                    self.right = SnailNumber(initial[char_id + 1:-1])
                    break
        else:
            #print("Type value")
            self.type = "value"
            self.value = int(initial)

    def __add__(self, other):
        return SnailNumber(f"[{self},{other}]")

    def reduce(self):
        string_representation = str(self)
        list_depth = 0
        needs_reducing = False
        for char_id, char in enumerate(string_representation):
            #print(f"{char_id}: {char} at {list_depth}")
            if char == "[":
                list_depth += 1
            elif char == "]":
                list_depth -= 1
            if list_depth >= 5:
                needs_reducing = True
                break
        print(string_representation)
        if needs_reducing:
            end_pair = string_representation.find("]", char_id)
            print("Creating exploding pair")
            print(string_representation[char_id:end_pair+1])
            exploding_pair = SnailNumber(string_representation[char_id:end_pair+1])
            next_number_pos = map(str.isdigit, string_representation[end_pair:])
            next_number_exists = False
            for number_id, char in enumerate(next_number_pos):
                if char == 1:
                    next_number_exists = True
                    break
            if next_number_exists:
                possible_values = [string_representation.find(",", end_pair + number_id), string_representation.find("]", end_pair + number_id)]
                end_number = min([value for value in possible_values if value >= 0])
                next_number = int(string_representation[end_pair+number_id:end_number])

            previous_number_pos = map(str.isdigit, string_representation[char_id::-1])
            previous_number_exists = False
            for previous_number_id, char in enumerate(previous_number_pos):
                if char == 1:
                    previous_number_exists = True
                    break
            #print(char_id)
            #print(previous_number_id)
            #print(string_representation.rfind("[", 0, char_id-previous_number_id))
            if previous_number_exists:
                start_number = max(string_representation.rfind(",", 0, char_id-previous_number_id),
                                   string_representation.rfind("[", 0, char_id-previous_number_id))+1
            else:
                start_number = char_id

            print(string_representation)
            print(string_representation[:start_number])
            new_string_representation = string_representation[:start_number]
            if previous_number_exists:
                end_previous_number = min(string_representation.find(",", start_number), string_representation.find("]", start_number))
                previous_number = int(string_representation[start_number:end_previous_number])
                new_string_representation += str(previous_number + exploding_pair.left.value) + string_representation[end_previous_number:char_id]
            else:
                new_string_representation += ""
            new_string_representation += "0"

            if next_number_exists:
                new_string_representation += string_representation[end_pair + 1:end_pair + number_id]
                new_string_representation += str(next_number + exploding_pair.right.value)
                new_string_representation += string_representation[end_number:]
            else:
                new_string_representation += string_representation[end_pair+1:]


            print("new string representation")
            print(new_string_representation)
            return SnailNumber(new_string_representation)
        else:
            # It might need splitting
            needs_splitting, value_to_split = self.needs_splitting()
            if needs_splitting:
                print(f"Splitting {value_to_split}")
                left_value = value_to_split.value // 2
                right_value = value_to_split.value - left_value
                value_to_split.type = "pair"
                value_to_split.value = None
                value_to_split.left = SnailNumber(str(left_value))
                value_to_split.right = SnailNumber(str(right_value))
                print("new string representation")
                print(self)
            return self

    def __repr__(self):
        if self.type == "value":
            return str(self.value)
        elif self.type == "pair":
            return f"[{self.left},{self.right}]"

    def __eq__(self, other):
        if self.type == "value":
            if isinstance(other, SnailNumber):
                if other.type == "value":
                    return self.value == other.value
                else:
                    return False
            if isinstance(other, int):
                return self.value == other
            else:
                return False
        elif self.type == "pair":
            if isinstance(other, SnailNumber):
                if other.type == "pair":
                    return self.left == other.left and self.right == other.right
                else:
                    return False
            elif isinstance(other, str):
                return self == SnailNumber(other)
            else:
                return False

    def __len__(self):
        return len(str(self))

    def needs_splitting(self):
        if self.type == "value":
            return (self.value > 9), self
        else:
            left_needs_split, left = self.left.needs_splitting()
            right_needs_split, right = self.right.needs_splitting()
            if left_needs_split:
                return True, left
            elif right_needs_split:
                return True, right
            else:
                return False, None

    def full_reduction(self):
        reduce = self.reduce()
        old = str(self)
        while reduce != old:
            old = str(reduce)
            reduce = reduce.reduce()
        return reduce

    def magnitude(self):
        if self.type == "value":
            return self.value
        else:
            return self.left.magnitude() * 3 + self.right.magnitude() * 2

basic_pair = SnailNumber("[1,2]")
print(basic_pair.type)
assert(basic_pair.left == 1)
assert(basic_pair.right == 2)

nested_pair = SnailNumber("[[1,2],3]")
assert(nested_pair.left.left == 1)

nested2_pair = SnailNumber("[9,[8,7]]")
assert(nested2_pair.right.left == 8)

nested3_pair = SnailNumber("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]")
assert(nested3_pair.right.right == 3)
assert(nested3_pair.left.right.left.left == 0)

sum_result = basic_pair + nested_pair
assert(sum_result.right.left.left == 1)
assert(sum_result.left.right == 2)

explode = SnailNumber("[[[[[9,8],1],2],3],4]")
print(explode)
explode = explode.reduce()
print(explode)
assert(explode.left.left.left.left == 0)
assert(explode == SnailNumber("[[[[0,9],2],3],4]"))

print("Create explode2")
explode2 = SnailNumber("[[[[1,[9,8]],2],3],4]")
explode2 = explode2.reduce()
assert(explode2 == SnailNumber("[[[[10,0],10],3],4]"))

print("Create explode3")
explode3 = SnailNumber("[1,[2,[3,[4,[9,8]]]]]")
explode3 = explode3.reduce()
assert(explode3 == SnailNumber("[1,[2,[3,[13,0]]]]"))

assert(SnailNumber("[7,[6,[5,[4,[3,2]]]]]").reduce() == SnailNumber("[7,[6,[5,[7,0]]]]"))
assert(SnailNumber("[[6,[5,[4,[3,2]]]],1]").reduce() == SnailNumber("[[6,[5,[7,0]]],3]"))
assert(SnailNumber("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]").reduce() == SnailNumber("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))
assert(SnailNumber("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]").reduce().reduce() == SnailNumber("[[3,[2,[8,0]]],[9,[5,[7,0]]]]"))

assert(SnailNumber("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]").reduce() == SnailNumber("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"))

assert(SnailNumber("[[[[4,3],4],4],[7,[[8,4],9]]]") + SnailNumber("[1,1]") == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce() == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce().reduce() == "[[[[0,7],4],[15,[0,13]]],[1,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce().reduce().reduce() == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce().reduce().reduce().reduce() == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce().reduce().reduce().reduce().reduce() == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").reduce().reduce().reduce().reduce().reduce().reduce() == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
assert(SnailNumber("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]").full_reduction() == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

assert(SnailNumber("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,0],[[9,10],0]]]]").reduce() == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[0,10]]]]")

from utils import read_file

lines = read_file("day18input-test")
snail_numbers = [SnailNumber(line.strip()) for line in lines]

total = snail_numbers[0]
for number in snail_numbers[1:]:
    total += number
    total = total.full_reduction()
assert(total == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

assert(SnailNumber("[9,1]").magnitude() == 29)
assert(SnailNumber("[[9,1],[1,9]]").magnitude() == 129)
assert(SnailNumber("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude() == 3488)

lines = read_file("day18input-test2")
snail_numbers = [SnailNumber(line.strip()) for line in lines]

total = snail_numbers[0]
for number in snail_numbers[1:]:
    total += number
    total = total.full_reduction()
assert(total.magnitude() == 4140)

lines = read_file("day18input")
snail_numbers = [SnailNumber(line.strip()) for line in lines]

total = snail_numbers[0]
for number in snail_numbers[1:]:
    total += number
    total = total.full_reduction()
print(total.magnitude())

current_max = -1
for left_number in snail_numbers:
    for right_number in snail_numbers:
        added = (left_number + right_number).full_reduction()
        if added.magnitude() > current_max:
            current_max = added.magnitude()
print(current_max)