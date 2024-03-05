# 🚧 dlt-init-openapi demo

Generates dlt pipelines from OpenAPI 3.x documents.

_This generator does not support OpenAPI 2.x FKA Swagger. If you need to use an older document, try upgrading it to
version 3 first with one of many available converters._


> 🕳️ This is only a demo.
> - will generate resources for all endpoints that return lists of objects
> - will use a few heuristics to find list wrapped in responses
> - will generate transformers from all endpoints that have a matching list resource (same object type returned)
> - will use a few heuristics to find the right object id to pass to the transformer
> - user can select endpoints using `questionary` lib in CLI
> - endpoints that have the most central data types (tables linking to many other tables) will be listed first
> - the structure of the code is not optimized!
> - there's no pagination added. use our GPT-4 playground to do that

**Generating a Pokemon dlt pipeline from Open API Spec 🚀**

<a href="https://www.loom.com/share/2806b873ba1c4e0ea382eb3b4fbaf808">
    <img style="max-width:450px;" src="https://cdn.loom.com/sessions/thumbnails/2806b873ba1c4e0ea382eb3b4fbaf808-with-play.gif">
  </a>
  

## Prior work
This is a heavily hacked fork of [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)

## Usage
1. You need `poetry` to install dependencies
```
poetry install
poetry shell
```

2. Create new `dlt` pipeline from [PokeAPI spec](https://raw.githubusercontent.com/cliffano/pokeapi-clients/main/specification/pokeapi.yml) and place it in the `pokemon-pipeline` 
```
dlt-init init pokemon --url https://raw.githubusercontent.com/cliffano/pokeapi-clients/ec9a2707ef2a85f41b747d8df013e272ef650ec5/specification/pokeapi.yml
```

3. After executing of the command, you can pick the endpoints that you want to add to your source and then load with the pipeline. The endpoints are grouped by returned data type (table) and ordered by centrality (a measure how many other tables, the given table links to):
```
? Which resources would you like to generate? (Use arrow keys to move, <space> to select, <a> to toggle, <i> to invert)
 
PokemonSpecies endpoints:

   ○ pokemon_species_list /api/v2/pokemon-species/
 » ○ pokemon_species_read /api/v2/pokemon-species/{id}/
 
EvolutionChain endpoints:

   ○ evolution_chain_list /api/v2/evolution-chain/
   ○ evolution_chain_read /api/v2/evolution-chain/{id}/
 
MoveAilment endpoints:

   ○ move_ailment_list /api/v2/move-ailment/
   ○ move_ailment_read /api/v2/move-ailment/{id}/
 
Move endpoints:

   ○ move_list /api/v2/move/
   ○ move_read /api/v2/move/{id}/
 
Pokemon endpoints:

   ○ pokemon_list /api/v2/pokemon/
   ○ pokemon_read /api/v2/pokemon/{id}/
```

4. Pick your endpoints and press **ENTER** to generate pipeline. Now you are ready to load data.

5. Enter the `pokemon-pipeline` folder and execute the `pipeline.py` script. This will load your endpoints to local `duckdb`. Below we use `enlighten` to show fancy progress bars:
```
cd pokemon-pipeline
PROGRESS=enlighten python pipeline.py
```

6. Inspect the pipeline to see what got loaded
```
$ dlt pipeline pokemon_pipeline info
Found pipeline pokemon_pipeline in /home/rudolfix/.dlt/pipelines
Synchronized state:
_state_version: 2
_state_engine_version: 2
pipeline_name: pokemon_pipeline
dataset_name: pokemon_data
default_schema_name: pokemon
schema_names: ['pokemon']
destination: dlt.destinations.duckdb

Local state:
first_run: False
_last_extracted_at: 2023-06-12T11:50:16.171872+00:00

Resources in schema: pokemon
pokemon_species_read with 8 table(s) and 0 resource state slot(s)

Working dir content:
Has 1 completed load packages with following load ids:
1686570616.17882

Pipeline has last run trace. Use 'dlt pipeline pokemon_pipeline trace' to inspect
```
7. Launch the streamlit app to preview the data (we copy a streamlit config to make it work on codespaces)
```
cp -r ../.streamlit .
pip install pandas streamlit
dlt pipeline pokemon_pipeline show
```

## What You Get
When you run the command above, following files will be generated:
1. `pokemon-pipeline` a folder with all the files
2. a folder `pokemon` with the Python module containing dlt source, resources and the Python client. 
3. `__init__.py` in that folder with the dlt source
4. the `pipeline.py` file that loads the resources to duckdb
5. `.dlt` folder with the `config.toml`

## What's next
There's still work needed to make things useful:
1. We will fully restructure the underlying Python client. We'll compress all the files in `pokemon/api` folder into a single, nice and extendable client.
2. We'll allow to easily add pagination and other injections into client. GPT-4 friendly
3. Many more heuristics to extract resources and their dependencies
4. Integration with existing `dlt init` command 


# 🚀 openapi-python-client docs
If you want to experiment, features below still work

## OpenAPI features supported

1. All HTTP Methods
1. JSON and form bodies, path and query parameters
1. File uploads with multipart/form-data bodies
1. float, string, int, date, datetime, string enums, and custom schemas or lists containing any of those
1. html/text or application/json responses containing any of the previous types
1. Bearer token security

## Configuration

You can pass a YAML (or JSON) file to openapi-python-client with the `--config` option in order to change some behavior.
The following parameters are supported:


### project_name_override and package_name_override

Pass the `source` in command line to create pipeline instead!

### field_prefix

When generating properties, the `name` attribute of the OpenAPI schema will be used. When the `name` is not a valid Python identifier (e.g. begins with a number) this string will be prepended. Defaults to "field\_". It will also be used to prefix fields in schema starting with "_" in order to avoid ambiguous semantics.

Example:

```yaml
field_prefix: attr_
```

### package_version_override

Specify the package version of the generated client. If unset, the client will use the version of the OpenAPI spec.

Example:

```yaml
package_version_override: 1.2.3
```

### post_hooks

In the config file, there's an easy way to tell `openapi-python-client` to run additional commands after generation. Here's an example showing the default commands that will run if you don't override them in config:

```yaml
post_hooks:
   - "autoflake -i -r --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports ."
   - "isort ."
   - "black ."
```

### http_timeout

By default, the timeout for retrieving the schema file via HTTP is 5 seconds. In case there is an error when retrieving the schema, you might try and increase this setting to a higher value.

[changelog.md]: CHANGELOG.md
[poetry]: https://python-poetry.org/
