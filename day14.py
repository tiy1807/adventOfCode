from utils import read_file
import datetime

begin = datetime.datetime.now()
lines = read_file("day14input")

class Rules(list):
    def add_rule(self, start, end):
        self.append(Rule(start, end))




class Rule:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Polymer:
    def __init__(self, initial):
        self.polymer = {}
        for pair in [initial[id:id + 2] for id in range(len(initial)-1)]:
            if self.polymer.get(pair):
                self.polymer[pair] += 1
            else:
                self.polymer[pair] = 1
        self.terminal_letters = [initial[0], initial[-1]]
        self.rules = None

    def add_rules(self, rules):
        self.rules = rules

    def apply_insertions(self):
        pairs_to_add = []
        new_polymer = {}
        for pair in self.polymer.keys():
            if self.polymer[pair] > 0:
                character = self.rules.get(pair)
                if character:
                    new_pairs = [pair[0] + character, character + pair[1]]
                    for new_pair in new_pairs:
                        #print(new_pair)
                        #if new_polymer.get(new_pair):
                        #    new_polymer[new_pair] += self.polymer[new_pair] + self.polymer[pair]
                        #else:
                        #    print("Added to be added later")
                        pairs_to_add.append((new_pair, self.polymer[pair]))
        for pair, amount in pairs_to_add:
            if new_polymer.get(pair):
                new_polymer[pair] += amount
            else:
                new_polymer[pair] = amount
        self.polymer = new_polymer

    def __repr__(self):
        return str(self.polymer)

    def count(self, letter):
        count = 0
        for pair in self.polymer:
            if pair == letter + letter:
                count += 2 * self.polymer[pair]
            elif letter in pair:
                count += self.polymer[pair]
        if letter in self.terminal_letters:
            count += 1
        count = count // 2
        return count

    def frequency(self):
        letters = set("".join(self.polymer.keys()))
        letter_frequency = {}
        for letter in letters:
            letter_frequency[letter] = self.count(letter)
        return letter_frequency


polymer = Polymer(lines[0].strip())
rules = {}
for line in lines[2:]:
    start, end = [t.strip() for t in line.split("->")]
    rules[start] = end
polymer.add_rules(rules)
for step in range(40):
    print(step)
    print(polymer)
    polymer.apply_insertions()

frequency = polymer.frequency()
print(polymer)
print(frequency)
print(max(frequency.values()) - min(frequency.values()))

end = datetime.datetime.now()
print(end-begin)
