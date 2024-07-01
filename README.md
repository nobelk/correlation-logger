# Correlation logger

Production-ready logging library for Python.
The aim here is to be able to use correlation ids for generating actionable production logs.
By including the correlation id within the method signature, it helps a team to standardize the correlation id based 
logging in the production code.
With the presence of correlation ids, it is possible to track events and errors across the service and application
boundaries.

## Example usage

service a --calls--> service b --calls--> service c with the correlation Id: 16db3469-7dde-442e-ae1f-5073f9b737c6.
All log files across the services will then contain this id in the logs allowing us to trace the impact of the chain of
service calls.

## Log types

The logs are published in two types of configurable log sinks:

1) Console
2) AWS cloudwatch logs It supports correlation ids or salt to perform detail tracing of the events.

# To activate virtual environment
`poetry shell`

# To build project
`poetry build`

# To test project
`poetry run pytest -v`

# Pypi project installation
`pip install correlation-logger`
