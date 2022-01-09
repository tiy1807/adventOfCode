from utils import read_file

lines = read_file("day16input")

class Packet:
    # Packet types
    LITERAL = 4
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    GREATER = 5
    LESS = 6
    EQUAL = 7

    # Length bit
    TOTAL_LENGTH_IN_BITS = 0
    NUMBER_OF_SUBPACKETS = 1

    def __init__(self, hex=None, binary=None):
        if hex:
            hex_to_bin = {"0" : "0000", "1" : "0001", "2" : "0010", "3": "0011", "4" : "0100", "5" : "0101",
                          "6" : "0110", "7" : "0111", "8" : "1000", "9" : "1001", "A" : "1010", "B" : "1011",
                          "C" : "1100", "D" : "1101", "E" : "1110", "F" : "1111"}
            self.binary = [int(char) for char in "".join(map(hex_to_bin.get, hex))]
        if binary:
            if isinstance(binary, str):
                self.binary = [int(char) for char in binary]
            else:
                self.binary = binary
        if self.type == self.LITERAL:
            self.value = []
            value_offset = 0
            is_last = False
            while not is_last:
                value = self.binary[6 + value_offset:11 + value_offset]
                self.value += value[1:]
                if value[0] == 0:
                    is_last = True
                else:
                    value_offset += 5
            self.binary = self.binary[:11 + value_offset]
        else:
            # Must be an operator packet
            self.packets = []
            if self.binary[6] == self.TOTAL_LENGTH_IN_BITS:
                self.length_of_subpackets = self.binary[7:22]
                packet_start = 22
                while packet_start < self.convert_to_decimal(self.length_of_subpackets) + 21:
                    self.packets.append(Packet(binary=self.binary[packet_start:]))
                    packet_start += self.packets[-1].total_bits

            elif self.binary[6] == self.NUMBER_OF_SUBPACKETS:
                self.number_of_subpackets = self.binary[7:18]
                packet_start = 18
                while (len(self.packets) < self.convert_to_decimal(self.number_of_subpackets)) and (sum(self.binary[packet_start:]) > 0 and len(self.binary[packet_start:]) >= 11):
                    self.packets.append(Packet(binary=self.binary[packet_start:]))
                    packet_start += self.packets[-1].total_bits
            self.binary = self.binary[:packet_start]

    @property
    def total_bits(self):
        return len(self.binary)

    @staticmethod
    def convert_to_decimal(binary):
        length = len(binary)-1
        return sum([(2**(length-i))*bit for i, bit in enumerate(binary)])

    @property
    def version(self):
        return self.convert_to_decimal(self.binary[:3])

    @property
    def type(self):
        return self.convert_to_decimal(self.binary[3:6])

    @property
    def decimal_value(self):
        if self.type == self.LITERAL:
            return self.convert_to_decimal(self.value)
        elif self.type == self.SUM:
            return sum([p.decimal_value for p in self.packets])
        elif self.type == self.PRODUCT:
            value = 1
            for product in self.packets:
                value = value * product.decimal_value
            return value
        elif self.type == self.MINIMUM:
            return min([p.decimal_value for p in self.packets])
        elif self.type == self.MAXIMUM:
            return max([p.decimal_value for p in self.packets])
        elif self.type == self.GREATER:
            if self.packets[0].decimal_value > self.packets[1].decimal_value:
                return 1
            else:
                return 0
        elif self.type == self.LESS:
            if self.packets[0].decimal_value < self.packets[1].decimal_value:
                return 1
            else:
                return 0
        elif self.type == self.EQUAL:
            if self.packets[0].decimal_value == self.packets[1].decimal_value:
                return 1
            else:
                return 0

    def get_all_packets(self):
        all_packets = []
        if self.type != self.LITERAL:
            all_packets.append(self)
            for packet in self.packets:
                all_packets += packet.get_all_packets()
        else:
            all_packets.append(self)
        return all_packets

    @property
    def version_sum(self):
        return sum([p.version for p in self.get_all_packets()])

hex_example = Packet(hex="D2FE28")
assert(hex_example.decimal_value == 2021)

example = Packet(binary="110100101111111000101000")
assert(Packet.convert_to_decimal([1, 1, 1]) == 7)
assert(example.version == 6)
assert(example.type == 4)
assert(example.decimal_value == 2021)

one_example = Packet(binary="11010001010")
assert(one_example.decimal_value == 10)

hex_example = Packet(binary="00111000000000000110111101000101001010010001001000000000")
assert(hex_example.version == 1)
assert(hex_example.type == 6)
assert(hex_example.packets[0].decimal_value == 10)
assert(hex_example.packets[1].decimal_value == 20)

number_sub_packets_example = Packet(binary="11101110000000001101010000001100100000100011000001100000")
assert(number_sub_packets_example.version == 7)
assert(number_sub_packets_example.type == 3)
print(number_sub_packets_example.number_of_subpackets)
assert(number_sub_packets_example.packets[0].decimal_value == 1)
assert(number_sub_packets_example.packets[1].decimal_value == 2)
assert(number_sub_packets_example.packets[2].decimal_value == 3)

nest_operators = Packet(hex="8A004A801A8002F478")
assert(nest_operators.packets[0].version == 1)
assert(nest_operators.packets[0].packets[0].version == 5)
assert(nest_operators.packets[0].packets[0].packets[0].type == 4)

print([p.version for p in nest_operators.get_all_packets()])
assert(nest_operators.version_sum == 16)

second_test = Packet(hex="620080001611562C8802118E34")
print(second_test.binary)
print(second_test.binary[:3])
print(second_test.binary[3:6])
print(second_test.binary[7:18])
print(second_test.binary[18:])
print(Packet.convert_to_decimal(second_test.number_of_subpackets))
print(second_test.packets)
print(second_test.packets[0].binary)
print([p.version for p in second_test.get_all_packets()])
assert(second_test.version_sum == 12)

third_test = Packet(hex="C0015000016115A2E0802F182340")
assert(third_test.version_sum == 23)

fourth_test = Packet(hex="A0016C880162017C3686B18A3D4780")
assert(fourth_test.version_sum == 31)

real_data = Packet(hex=lines[0].strip())
print(real_data.version_sum)

print("Adding test")
sum1 = Packet(hex="C200B40A82")
print(sum1.binary)
print(sum1.version)
print(sum1.type)
print(sum1.decimal_value)
assert(sum1.decimal_value == 3)

product = Packet(hex="04005AC33890")
print(product.decimal_value)
assert(product.decimal_value == 54)

min1 = Packet(hex="880086C3E88112")
print(min1.decimal_value)
assert(min1.decimal_value == 7)

max1 = Packet(hex="CE00C43D881120")
print(max1.decimal_value)
assert(max1.decimal_value == 9)

less = Packet(hex="D8005AC2A8F0")
print(less.decimal_value)
assert(less.decimal_value == 1)

greater = Packet(hex="F600BC2D8F")
print(greater.decimal_value)
assert(greater.decimal_value == 0)

equal = Packet(hex="9C005AC2F8F0")
print(equal.decimal_value)
assert(equal.decimal_value == 0)

equal2 = Packet(hex="9C0141080250320F1802104A08")
print(equal2.decimal_value)
assert(equal2.decimal_value == 1)

print(real_data.decimal_value)
