class Product:
    def __init__(self, product_id, product_name, price, purpose, architecture, dimensions, weight, quantity_sold,
                 supplied_by):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.purpose = purpose
        self.architecture = architecture
        self.dimensions = dimensions
        self.weight = weight
        self.quantity_sold = quantity_sold
        self.supplied_by = supplied_by


class Ram:
    def __init__(self, product_id, capacity, memory_speed, ram_type):
        self.product_id = product_id
        self.capacity = capacity
        self.memory_speed = memory_speed
        self.ram_type = ram_type


class PcCase:
    def __init__(self, product_id, motherboard_support, io_ports, fan_support, hdd_support, psu_support):
        self.product_id = product_id
        self.motherboard_support = motherboard_support
        self.io_ports = io_ports
        self.fan_support = fan_support
        self.hdd_support = hdd_support
        self.psu_support = psu_support


class CPU:
    def __init__(self, product_id, cpu_socket, speed, processor_count):
        self.product_id = product_id
        self.cpu_socket = cpu_socket
        self.speed = speed
        self.processor_count = processor_count


class GPU:
    def __init__(self, product_id, memory_size, memory_speed):
        self.product_id = product_id
        self.memory_size = memory_size
        self.memory_speed = memory_speed


class PcCooler:
    def __init__(self, product_id, cpu_socket, heatsink_dimensions, fan_dimensions, rotation_speed, power):
        self.product_id = product_id
        self.cpu_socket = cpu_socket
        self.heatsink_dimensions = heatsink_dimensions
        self.fan_dimensions = fan_dimensions
        self.rotation_speed = rotation_speed
        self.power = power


class Motherboard:
    def __init__(self, product_id, cpu_socket, chipset, ram_slots, ram_capacity, ram_type):
        self.product_id = product_id
        self.cpu_socket = cpu_socket
        self.chipset = chipset
        self.ram_slots = ram_slots
        self.ram_capacity = ram_capacity
        self.ram_type = ram_type


class Storage:
    def __init__(self, product_id, type, capacity, rotation_speed):
        self.product_id = product_id
        self.type = type
        self.capacity = capacity
        self.rotation_speed = rotation_speed


class PSU:
    def __init__(self, product_id, power):
        self.product_id = product_id
        self.power = power


class System:
    def __init__(self, product_id, cpu, ram_size, gpu, hdd_size, operating_system):
        self.product_id = product_id
        self.cpu = cpu
        self.ram_size = ram_size
        self.gpu = gpu
        self.hdd_size = hdd_size
        self.operating_system = operating_system
