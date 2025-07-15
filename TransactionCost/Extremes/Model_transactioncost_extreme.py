import copy

import mesa
from mesa.space import NetworkGrid
import networkx as nx
import matplotlib.pyplot as plt
import csv
import random

#trading behaviors
def aggressive_trade(agent1, agent2):
    """Aggressive trading behavior: tries to trade as much as possible."""
    # This agent tries to trade all available goods.
    if len(agent1.goods_list) == 0:
        return 0  # No goods to trade
    return min(len(agent1.goods_list), random.randint(1, len(agent1.goods_list))) #returns the value

def conservative_trade(agent1, agent2):
    """Conservative trading behavior: trades minimal amounts."""
    # This agent trades only 1 or 2 goods at most.
    if len(agent1.goods_list) == 0:
        return 0  # No goods to trade
    return min(len(agent1.goods_list), random.randint(1, 2)) #returns the value

def random_trade(agent1, agent2):
    """Random trading behavior: trades a random number of goods."""
    # This agent trades a random number of goods from 1 to half of the goods it has.
    if len(agent1.goods_list) == 0:
        return 0  # No goods to trade
    return min(len(agent1.goods_list), random.randint(1, max(1, len(agent1.goods_list) // 2))) #returns the value


#trading_behavior_list =random.choice([aggressive_trade, conservative_trade, random_trade])

class Goods:
    def __init__(self, goods_list):
        self.goods_list = goods_list  # List of tuples (name, quantity, price)



#1. create agent groups

#create agents from Adriatic
class AgentAdria(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Adria"
        self.type_id = 0
        self.goods_list = [("AdriaticPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False

#create agents from Aegean
class AgentAegean(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Aegean"
        self.type_id = 1
        self.goods_list = [("AegeanPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Baetica
class AgentBaetica(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Baetica"
        self.type_id = 2
        self.goods_list = [("BaeticanPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from EM
class AgentEM(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Eastern Mediterranean"
        self.type_id = 3
        self.goods_list = [("EMPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Egypt
class AgentEgypt(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Egypt"
        self.type_id = 4
        self.goods_list = [("EgyptianPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Gallia
class AgentGallia(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Gallia"
        self.type_id = 5
        self.goods_list = [("GallicPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Iberian Peninsula
class AgentIberia(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Iberian Peninsula"
        self.type_id = 10
        self.goods_list = [("IberianPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Italy
class AgentItaly(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Italy"
        self.type_id = 6
        self.goods_list = [("ItalianPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from North Africa
class AgentNA(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "North Africa"
        self.type_id = 7
        self.goods_list = [("NAPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Tarraconensis
class AgentTarr(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Tarraconensis"
        self.type_id = 8
        self.goods_list = [("TarrPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#create agents from Western Mediterranean
class AgentWM(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 500
        self.type = "Western Mediterranean"
        self.type_id = 9
        self.goods_list = [("WMPottery", 1, 1)] * 10
        self.active = True
        self.agent_behavior = None
        self.trades_per_step = 0
        self.has_traded = False

    def step(self):
        '''Moves the agent to a randomly chosen neighboring node.'''
        if self.wealth <= 0:
            self.active = False
            return

        # Reset the has_traded flag so the agent can trade again
        self.has_traded = False

        # Get a list of all neighboring nodes
        neighbors = list(self.model.G.neighbors(self.pos))

        if neighbors:
            # Randomly choose one neighbor to move to
            chosen_move = random.choice(neighbors)
            edge_weight = self.model.G.edges[self.pos, chosen_move]['weight']

            # Deduct the travel cost and update position
            self.last_traveled_edge_weight = edge_weight
            self.model.grid.move_agent(self, chosen_move)
            self.wealth -= edge_weight

            # If the agent runs out of wealth after moving, deactivate it
            if self.wealth <= 0:
                self.active = False


#2. create model
class TestModelINTEST(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, G, agents_per_node, agent_behaviors=None):
        """
        Initialize the model.

        :param G: The graph.
        :param agents_per_node: Dictionary specifying agents per node.
        :param agent_behaviors: Dictionary of agent behaviors to reuse across runs.
        """
        self.G = G
        self.grid = NetworkGrid(G)
        self.current_id = 0
        self.schedule = mesa.time.RandomActivation(self)
        self.agent_behaviors = agent_behaviors or {}  # Use existing behaviors or create new ones

        for node in G.nodes:
            agent_class = None
            if node == 0:
                agent_class = AgentAdria
            elif node == 1:
                agent_class = AgentAegean
            elif node == 2:
                agent_class = AgentBaetica
            elif node == 3:
                agent_class = AgentEM
            elif node == 4:
                agent_class = AgentEgypt
            elif node == 5:
                agent_class = AgentGallia
            elif node == 6:
                agent_class = AgentItaly
            elif node == 7:
                agent_class = AgentIberia
            elif node == 8:
                agent_class = AgentNA
            elif node == 9:
                agent_class = AgentTarr
            elif node == 10:
                agent_class = AgentWM

            num_agents = agents_per_node.get(node, 0)
            for _ in range(num_agents):
                agent_id = self.next_id()

                # Assign fixed trade behavior if available, else create new
                if agent_id in self.agent_behaviors:
                    behavior = self.agent_behaviors[agent_id]
                else:
                    behavior = random.choice([aggressive_trade, conservative_trade, random_trade])
                    self.agent_behaviors[agent_id] = behavior

                agent = agent_class(unique_id=agent_id, model=self)
                agent.goods_list = copy.deepcopy(agent.goods_list)
                agent.agent_behavior = behavior  # Use fixed behavior
                self.grid.place_agent(agent, node)
                self.schedule.add(agent)

    def next_id(self):
        """Return the next unique ID for an agent."""
        self.current_id += 1
        return self.current_id

    def get_num_agents(self):
        """Return the current number of agents in the model."""
        return len(self.schedule.agents)

    def trade(self, agent1, agent2):
        """
        Handle the trading logic between two agents.
        For each good that is traded, select the cheapest of three randomly chosen options from the receiver's inventory.
        """
        if not agent1.active or not agent2.active:
            print(f"Trade skipped: Agent {agent1.unique_id} or Agent {agent2.unique_id} is inactive.")
            return

        if agent1.has_traded or agent2.has_traded:
            print(f"Trade skipped: Agent {agent1.unique_id} or Agent {agent2.unique_id} has already traded.")
            return

        # Get trade amounts based on behaviors
        trade_amount1 = agent1.agent_behavior(agent1, agent2)
        trade_amount2 = agent2.agent_behavior(agent2, agent1)

        # Randomly select goods to trade based on trade amounts
        goods_traded_by_agent1 = random.sample(agent1.goods_list, min(trade_amount1, len(agent1.goods_list)))
        goods_traded_by_agent2 = random.sample(agent2.goods_list, min(trade_amount2, len(agent2.goods_list)))

        # Process goods traded by agent1
        for good in goods_traded_by_agent1:
            good_name, good_quantity, good_price = good

            if agent2.wealth >= good_price:  # Ensure agent2 can afford the good
                # Randomly choose up to 3 options from agent2's goods list to trade
                options = random.sample(agent2.goods_list, min(3, len(agent2.goods_list)))
                if options:
                    # Select the cheapest good from the options
                    cheapest_option = min(options, key=lambda x: x[2])  # Based on price
                    option_name, option_quantity, option_price = cheapest_option

                    # Execute the trade: agent1 -> agent2
                    agent2.wealth -= good_price
                    agent1.wealth += good_price
                    # Remove or reduce quantity in agent1's inventory
                    for i, (name, quantity, price) in enumerate(agent1.goods_list):
                        if name == good_name:
                            if quantity > 1:
                                agent1.goods_list[i] = (name, quantity - 1, price)
                            else:
                                del agent1.goods_list[i]
                            break
                    # Add the good to agent2's inventory
                    agent2.goods_list.append((good_name, 1, good_price))

                    # Remove or reduce the cheapest good in agent2's inventory
                    for i, (name, quantity, price) in enumerate(agent2.goods_list):
                        if name == option_name:
                            if quantity > 1:
                                agent2.goods_list[i] = (name, quantity - 1, price)
                            else:
                                del agent2.goods_list[i]
                            break
                    # Add the cheapest good to agent1's inventory
                    agent1.goods_list.append((option_name, 1, option_price))

        # Process goods traded by agent2
        for good in goods_traded_by_agent2:
            good_name, good_quantity, good_price = good

            if agent1.wealth >= good_price:  # Ensure agent1 can afford the good
                # Randomly choose up to 3 options from agent1's goods list to trade
                options = random.sample(agent1.goods_list, min(3, len(agent1.goods_list)))
                if options:
                    # Select the cheapest good from the options
                    cheapest_option = min(options, key=lambda x: x[2])  # Based on price
                    option_name, option_quantity, option_price = cheapest_option

                    # Execute the trade: agent2 -> agent1
                    agent1.wealth -= good_price
                    agent2.wealth += good_price
                    # Remove or reduce quantity in agent2's inventory
                    for i, (name, quantity, price) in enumerate(agent2.goods_list):
                        if name == good_name:
                            if quantity > 1:
                                agent2.goods_list[i] = (name, quantity - 1, price)
                            else:
                                del agent2.goods_list[i]
                            break
                    # Add the good to agent1's inventory
                    agent1.goods_list.append((good_name, 1, good_price))

                    # Remove or reduce the cheapest good in agent1's inventory
                    for i, (name, quantity, price) in enumerate(agent1.goods_list):
                        if name == option_name:
                            if quantity > 1:
                                agent1.goods_list[i] = (name, quantity - 1, price)
                            else:
                                del agent1.goods_list[i]
                            break
                    # Add the cheapest good to agent2's inventory
                    agent2.goods_list.append((option_name, 1, option_price))

        # Mark both agents as having traded
        agent1.has_traded = True
        agent2.has_traded = True

        print(
            f"Trade completed: Agent {agent1.unique_id} traded {len(goods_traded_by_agent1)} goods "
            f"with Agent {agent2.unique_id}."
        )
        print(
            f"Post-trade: Agent {agent1.unique_id} Wealth={agent1.wealth}, Goods={len(agent1.goods_list)}; "
            f"Agent {agent2.unique_id} Wealth={agent2.wealth}, Goods={len(agent2.goods_list)}"
        )

        # Mark both agents as having traded
        agent1.has_traded = True
        agent2.has_traded = True

    def meet_agents(self):
        """Facilitate meetings between active agents on the same node considering transaction costs."""
        for node in self.G.nodes:
            # Get all active agents on the current node
            agents_on_node = [agent for agent in self.schedule.agents if agent.pos == node and agent.active]
            print(f"Number of active agents on node {node}: {len(agents_on_node)}")

            # Continue pairing agents until less than 2 agents remain
            while len(agents_on_node) > 1:
                # Randomly select up to 5 agents from the list
                if len(agents_on_node) > 5:
                    selected_agents = random.sample(agents_on_node, 5)
                else:
                    selected_agents = agents_on_node

                # Compute transaction costs for all possible pairs in the selected subset
                pair_costs = []
                for i in range(len(selected_agents)):
                    for j in range(i + 1, len(selected_agents)):
                        agent1 = selected_agents[i]
                        agent2 = selected_agents[j]
                        # Transaction cost: 1 if same type, otherwise 5
                        cost = 1 if agent1.type_id == agent2.type_id else 50

                        pair_costs.append((cost, agent1, agent2))

                # If no pairs are available, break
                if not pair_costs:
                    break

                # Find the pair(s) with the minimum transaction cost
                pair_costs.sort(key=lambda x: x[0])  # Sort by cost
                min_cost = pair_costs[0][0]
                min_cost_pairs = [pair for pair in pair_costs if pair[0] == min_cost]

                # Randomly select one pair among those with minimum cost
                cost, agent1, agent2 = random.choice(min_cost_pairs)

                # Remove selected agents from the list
                agents_on_node.remove(agent1)
                agents_on_node.remove(agent2)

                # Proceed with the trade
                self.trade(agent1, agent2)
                print(
                    f"Trade successful between Agent {agent1.unique_id} and Agent {agent2.unique_id} with cost {cost}")


    def step(self):
        """Advance the model by one step and subtract the edge weight from its wealth."""
        for agent in self.schedule.agents:
            agent.trades_per_step = 0
            agent.step()

        self.meet_agents()

