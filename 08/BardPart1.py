def read_network_and_instructions(filename):
  """
  Reads the network and instructions from a file.

  Args:
    filename: The filename of the input file.

  Returns:
    A tuple containing the network dictionary and the instructions string.
  """
  with open(filename) as f:
    instructions = f.readline().strip()
    network_data = f.readlines()
  network = {}
  for line in network_data:
    if len(line.strip()) == 0: continue #I had to do this part for the AI
    node, connections = line.strip().split(" = ")
    left, right = connections.strip()[1:-1].split(", ") # better way than mine for getting rid of ()
    network[node] = (left, right)
  return network, instructions

def navigate_network(network, instructions, start_node="AAA"):
  """
  Navigates the network based on the instructions.

  Args:
    network: A dictionary representing the network.
    instructions: A string containing the left/right instructions.
    start_node: The starting node in the network.

  Returns:
    The number of steps required to reach the target node.
  """
  current_node = start_node
  steps = 1
  instruction_index = 0 # AI had to create this variable because it didn't iterate the steps 1 last time before reporting answer
  while True:
    instruction = instructions[instruction_index % len(instructions)]
    if instruction == "L":
      next_node = network[current_node][0]
    else:
      next_node = network[current_node][1]
    if next_node == "ZZZ":
      return steps
    current_node = next_node
    steps += 1
    instruction_index += 1

def main():
  network, instructions = read_network_and_instructions(r"C:\Users\etreq\Advent of Code\2023\08\input.txt")
  steps = navigate_network(network, instructions)
  print(f"It takes {steps} steps to reach ZZZ.")

if __name__ == "__main__":
  main()