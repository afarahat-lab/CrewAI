import os, yaml
from pathlib import Path
from crewai import Agent, Crew, CrewOutput, Task
from crewai.types.streaming import CrewStreamingOutput
from crewai.llm import LLM
from .trello_tools import BoardDataFetcherTool, CardDataFetcherTool

def load_yaml_config(file_path: str) -> dict:
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / file_path
    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_configs() -> dict:
    config_files = {"agents": "agents.yaml", "tasks": "tasks.yaml"}
    configs = {}
    for key, file_path in config_files.items():
        configs[key] = load_yaml_config(file_path)
    return configs


def create_crew(llm: LLM, verbose: bool = False) -> Crew:
    # Load configurations from YAML files
    configs: dict = load_configs()

    # Assign loaded configurations to specific variables
    agents_config = configs["agents"]
    tasks_config = configs["tasks"]

    agents: dict[str, Agent] = {} # This will hold our agent instances
    tasks: list[Task] = []  # This will hold our task instances

    # Creating Agents
    for agent_name in agents_config:
        agent_config = agents_config[agent_name]
        agent_config["llm"] = llm  # Inject the LLM into each agent's config

        if agent_config.get("tools_names") is not None:
            agent_config["tools"] = []  # Initialize the tools list in the agent config

            for tool_name in agent_config["tools_names"]:
                tool_class = globals().get(tool_name)  # Load tool config from YAML
                if tool_class is not None:
                    agent_config["tools"].append(tool_class())  # Add the tool to the agent

        agent = Agent(config=agent_config)
        agents[agent_name] = agent

    # Creating Tasks
    for task_name in tasks_config:
        task_config = tasks_config[task_name]
        
        if task_config.get("output_pydantic") is not None:
            task_config["output_pydantic"] = locals().get(task_config["output_pydantic"])  # Specify the structured output for this task

        task = Task(config=task_config, agent=agents[task_config["agent"]])  # Assigning the first agent for simplicity
        tasks.append(task)

    # resource_allocation = Task(
    #     config=tasks_config["resource_allocation"],
    #     agent=resource_allocation_agent,
    #     output_pydantic=ProjectPlan,  # This is the structured output we want
    # )

    return Crew(
        agents=list(agents.values()),  # Pass the list of agent instances
        tasks=tasks,  # Pass the list of task instances
        verbose=verbose,
    )


def compile_inputs() -> dict:
    return load_yaml_config("inputs.yaml")  # Load inputs from YAML file


def run_crew(llm: LLM, verbose: bool = False) -> CrewOutput | CrewStreamingOutput:
    crew = create_crew(llm=llm, verbose=verbose)
    return crew.kickoff(inputs=compile_inputs())
