# Trees Everywhere

The "Trees Everywhere" project has the objective of creating a database of
planted trees by volunteers scattered around the world.

The user can join a group of other users, and all of them can see all the trees
that were planted by the group of users of the same account.

It is possible to see the project documentation in the `docs` directory, at the
root of the project. To compile, see the `docs/README.md` file.

## Dependencies
- Bash
- Make
- Docker
- Docker Compose
- Python 3.10+ (with `pip` support)

## Project execution commands
```bash
# To run the project using Docker (with django + postgresl in docker)
make start

# To run the project partially native (postgresl in docker, but django in native)
make start-native

# To run tests
make test

# To compile the documentation
make docs
```

## Have you made any changes to the database?

```bash
# In case you have made any changes to the structure of any model, you will need
# to check for necessary database changes.
# To do this, run:
make migrate

# If you have made changes to the database data, and want to make
# the information "persistent" so that the next developer has access to it,
# you can re-generate the "fixtures" file with the command:
make update-fixture

# If you wish to load the information from the fixture file into the database,
# run the command:
make load-fixture
```

## Troubleshooting

If you are running the project on some macOS machine with M1 (ARM) processor, it is possible that the project
cant be executed. To solve this problem, run the following steps in the terminal before running the project:
```bash
# Remove the generated files, if any
make clean

# Ensure that the database (local) will be completely without data
rm -rf db_data

# Configure docker to use arm64 versions of the images (including postgres)
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Rebuild all images and start the application
make start
```

## Authors

- [@jovitor123jv](https://www.github.com/joaovitor123jv)

