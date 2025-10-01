# Current Stage:

We're currently able to generate these docs:

Doc Structure:
├── docs/
   └── cod_mod_reports/
      └── cod_mod_functional_user_journeys.md
      └── cod_mod_data_layer.md
   └── context_docs/
      └── context_doc_1
      └── context_doc_2
      └── context_doc_n....
   └── user_journeys/
      └── user_journey_1
      └── user_journey_2
      └── user_journey_n ....
   └── database_design/
      └── database_definition.md
   └── api_design/
      └── api-dependencies.md
      └── api-definition.md
      └── api-plan.md
      └── api-design.md
   └── infra_design/
   

# Next steps

Using prompts. Generate a detail API design doc, that covers building the api.

* The Backend stack
  * Language and Framework (if you're familiar with node, us that)
  * What package management is used (assume npm or something else)
  * See if you can prompt the model to build user and authentication APIs as per `api_design/api_plan.md`
  

