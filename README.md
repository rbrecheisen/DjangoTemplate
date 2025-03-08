# DjangoTemplate
Template project for Django apps by Rbeesoft

## Tasks, pipelines and viewers
A task is a process that takes one or more filesets as input and produces a single fileset
as output. A pipeline is simply a collection of tasks that are executed in sequence. A 
viewer is a process that renders a single fileset visually. Viewers have their own set of
HTML pages and render functions. 

Task, pipeline and viewer pages can display errors (in red).

Tasks are executed in the background (using threading). The task manager runs tasks
individually. Pipelines use the task manager to execute a sequence of tasks. Each task
has to wait for the previous task to finish. How do I do that? Maybe the task manager
should have a function run_pipeline(config) that does this. The task manager knows when
a task is finished and can execute the next one. 

### Example tasks, pipelines and viewers
Tasks:
======
- RetrieveDataFromCastorTask
    - Inputs: None
    - Parameters:
        - Client ID
        - Cilent secret
        - Study name
    - Outputs:
        - Records
        - Field definitions
        - Option groups

- CreateSqlFromCastorDataTask
    - Inputs:
        - Records
        - Field definitions
        - Option groups
    - Parameters:
        - Table name
        - Column names to include
    - Output:
        - Database definition (SQL)

- CreateSqlQueryTask
    - Inputs: None
    - Parameters: None
    - Output: 
        - Query file (SQL)

- ExecuteSqlQueryTask
    - Inputs:
        - Fileset database .sql
        - Fileset query .sql
    - Parameters:
        - Output format (CSV, JSON)
    - Output:
        - Result set (dataframe? CSV?)

# References
- https://chatgpt.com/c/67cc7f9b-7518-800b-8713-4258670fa88c (How to dynamically create a SQLite3 and PostgreSQL database from a .sql file)