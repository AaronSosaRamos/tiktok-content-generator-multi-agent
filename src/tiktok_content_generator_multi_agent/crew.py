from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    SerperDevTool,
	ScrapeWebsiteTool
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TiktokContentGeneratorMultiAgent():
	"""TiktokContentGeneratorMultiAgent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def tiktok_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['tiktok_researcher'],
			verbose=True,
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
		)

	@agent
	def tiktok_content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['tiktok_content_creator'],
			verbose=True
		)
	
	@agent
	def tiktok_visual_consultant(self) -> Agent:
		return Agent(
			config=self.agents_config['tiktok_visual_consultant'],
			verbose=True
		)
	
	@agent
	def final_output_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['final_output_generator'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def content_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['content_creation_task'],
		)
	
	@task
	def visual_consulting_task(self) -> Task:
		return Task(
			config=self.tasks_config['visual_consulting_task'],
		)

	@task
	def final_output_task(self) -> Task:
		return Task(
			config=self.tasks_config['final_output_task'],
			output_file='output/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TiktokContentGeneratorMultiAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
