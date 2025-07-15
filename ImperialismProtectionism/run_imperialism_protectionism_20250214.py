from model_imperialism_protectionism_20250214 import TestModelINTEST
import networkx as nx
import csv
from collections import defaultdict
import time
import pandas as pd
import os

# Add graph
G = nx.Graph()

# Read the CSV file and add edges to the graph
with open('days_network_full.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=';')
    for line in reader:
        source, target, weight = map(float, line)
        G.add_edge(source, target, weight=weight)


# add incoming customs graph
incoming_customs_network = nx.Graph()
# Read the CSV file and add edges to the graph
with open('incoming_customs_network.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=';')
    for line in reader:
        source, target, weight = map(float, line)
        incoming_customs_network.add_edge(source, target, weight=weight)

# add outgoing customs graph
outgoing_customs_network = nx.Graph()
# Read the CSV file and add edges to the graph
with open('outgoing_customs_network.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=';')
    for line in reader:
        source, target, weight = map(float, line)
        outgoing_customs_network.add_edge(source, target, weight=weight)


# Define the number of agents for each node
agents_per_node = {i: 10 for i in range(11)}  # 10 agents per node, 11 nodes

# Number of runs
num_runs = 10
output_files = []


def run_model(run_number, fixed_agent_behaviors=None):
    # Initialize the model
    starter_model = TestModelINTEST(G, agents_per_node, incoming_customs_network, outgoing_customs_network, agent_behaviors=fixed_agent_behaviors)

    # Save agent behaviors if this is the first run
    if fixed_agent_behaviors is None:
        fixed_agent_behaviors = starter_model.agent_behaviors

    step_count = 0
    max_steps = 3000  # Safety mechanism to prevent infinite loop

    while step_count < max_steps:
        active_agents = [agent for agent in starter_model.schedule.agents if agent.active]
        print(f"Run {run_number}, Step {step_count}: Active Agents = {len(active_agents)}", flush=True)
        if not active_agents:
            break
        starter_model.step()
        step_count += 1

    # Output the final state of each agent
    output_filename = f'Runs/agents_imperialism_protectionism_run_{run_number}_20250214.csv'
    output_files.append(output_filename)

    all_goods = set()
    for agent in starter_model.schedule.agents:
        for good_name, _, _ in agent.goods_list:
            all_goods.add(good_name)

    fieldnames = ['Run', 'Step Count', 'Agent ID', 'Agent Class', 'Total Wealth', 'Trade Behavior', 'Active'] + list(all_goods)

    # Write to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for agent in starter_model.schedule.agents:
            goods_summary = defaultdict(int)
            for good_name, good_quantity, _ in agent.goods_list:
                goods_summary[good_name] += good_quantity

            row = {
                'Run': run_number,
                'Step Count': step_count,
                'Agent ID': agent.unique_id,
                'Agent Class': agent.type,
                'Total Wealth': agent.wealth,
                'Trade Behavior': agent.agent_behavior.__name__ if agent.agent_behavior else "None",
                'Active': agent.active  # Include active status
            }
            for good in all_goods:
                row[good] = goods_summary.get(good, 0)
            writer.writerow(row)

    print(f"Run {run_number} completed. Results saved to: {output_filename}")
    return fixed_agent_behaviors



# Run the model multiple times
fixed_agent_behaviors = None
if not os.path.exists('Runs'):
    os.makedirs('Runs')

for run in range(1, num_runs + 1):
    print(f"Starting Run {run}")
    fixed_agent_behaviors = run_model(run, fixed_agent_behaviors)
    time.sleep(0.5)

print("All runs completed. Aggregating results...")

# Combine all output files into a single dataframe
all_dataframes = []
for file in output_files:
    if os.path.exists(file):
        print(f"Reading file: {file}")
        df = pd.read_csv(file)
        all_dataframes.append(df)
    else:
        print(f"Warning: File not found: {file}")

# Concatenate all runs
if all_dataframes:
    combined_data = pd.concat(all_dataframes, ignore_index=True)

    # Group by Agent ID and calculate averages (includes Trade Behavior and Active columns)
    average_data_by_id = combined_data.drop(columns=['Run', 'Step Count']).groupby(
        ['Agent ID', 'Agent Class', 'Trade Behavior', 'Active']).mean()

    # Save the averages by Agent ID to a new CSV file
    id_average_output_file = 'Runs/agents_imperialism_protectionism_id_averages_20250214.csv'
    average_data_by_id.to_csv(id_average_output_file)
    print(f"Averages by Agent ID saved to: {id_average_output_file}")

    # Group by Agent Class and calculate averages across all trade behaviors
    average_data_by_class = combined_data.drop(columns=['Run', 'Step Count', 'Agent ID', 'Trade Behavior', 'Active']).groupby(
        ['Agent Class']).mean()

    # Save the class-based averages to a new CSV file
    class_average_output_file = 'Runs/agents_imperialism_protectionism_class_averages_20250214.csv'
    average_data_by_class.to_csv(class_average_output_file)
    print(f"Averages by Agent Class saved to: {class_average_output_file}")
else:
    print("No files to aggregate. Check the file generation process.")

