# Code to Code - Proof of Concept

PoC for a Code-2-Code solution based on Google tools.

The solution is built to take in a piece of legacy code, building documentation from a functional perspective and rebuilding the code on a modern stack.

This is not code-modernization solution, we are not transforming code from one language to another, instead we are re-building the app by documenting the existing codebase and rebuilding the code from those documentation. 

This approach means that the solution:

* Builds out documentation from code for human (and agent) consumption
* Allows for major re-architecture and code level changes
* Produces design documents that can be reviewed and changed before execution
* Creates a detailed plan for execution

## Design Decisions

* The documentation is in markdown format. This format is ideal for agent/LLM consumption, and can be easily made human readable through the right tools.
* The documentation are broken into chunks -- e.g. instead of producing a single big API design document, we produce 4 markdown files that breakdown design, dependencies, definition and implementation plan. Again, this is done for easier consumption of the tools.
* Docs are stored in `docs` folder
* Currently we use taskmaster to convert the last PRD into tasks, but the tool is flaky and sometimes fails. We may change this in the future.

## High Level Design

### Creation of documentations

![Step 1](assets/step-1.jpg)

### Creation of design documents and execution

![Step 2](assets/step-2.jpg)


## Step 0:

### Context Docs

The Context for the design, context docs are important to set the context for prompts.

* CodMod context file (`docs/context_docs/codmod-context.md`) - provides the context for CodMod, specifying the high-level user journeys. (e.g. outline the top 5 user journeys in the context doc etc)
* Example User Journey (`docs/example_user_journey.md`) - example document for user journey
* Architecture Principles (`docs/context_docs/architecture_principles.md`) - Outlines the high level architecture/design principles important for creating the design documents.


## Step 1:

```bash
codmod create full -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_detailed_journeys.md \
--context-file docs/context_docs/codmod-context.md
```

```bash
codmod create data-layer -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_data_layer.md
```



## Step 3:

  $ python gen_docs.py

This step generates the requiremtns and design documents:

* User Journeys (`docs/user_journeys`)
* Business Requirement Documents (`docs/brds`)
* API Design Documents (`docs/api_design`)
  * API Definitions (`docs/api_deifintion.md`) - Endpoints, request parameters, response parameters, etc
  * API dependencies (`docs/api_dependencies.md`) - Dependecies between different endpoints
  * API Detail Design (`docs/api_detail_design.md`) - The design of the API
  * API Plan (`docs/api_plan.md`) - Breaking down the API deployment to multple phases


  $ uv venv
  $ source ./venv/bin/activate
  $ uv sync

## Step 5: Consolidation

  $ python gen_fs.py
