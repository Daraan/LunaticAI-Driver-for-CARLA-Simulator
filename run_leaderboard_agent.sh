# NOTE: This file is supposed to run from the leaderboard-agent branch and with a setup from doc/leadearbord_requirements

export LEADERBOARD_ROOT=~/TeamProject/leaderboard

# Parameterization settings. These will be explained in 2.2. Now simply copy them to run the test.
export REPETITIONS=1
# If this variable is set to anything greater than 1 the engine will print the complete state of the simulation for debugging purposes.
# if > 1 DEBUG_CHECKPOINT_ENDPOINT must also be set
export DEBUG_CHALLENGE=1
export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=MAP

# Define Team files
export TEAM_AGENT_ROOT=${PWD}
export TEAM_AGENT=${TEAM_AGENT_ROOT}/agents/leaderboard_agent.py
export TEAM_CONFIG=${TEAM_AGENT_ROOT}/conf/launch_config.yaml

export SCENARIO_RUNNER_ROOT=${TEAM_AGENT_ROOT}/scenario_runner
export PYTHONPATH=${TEAM_AGENT_ROOT}:${LEADERBOARD_ROOT}:${SCENARIO_RUNNER_ROOT}:${PYTHONPATH}

# Choose Route

# Alternative Route for faster testing on Town 10
export ROUTES=${SCENARIO_RUNNER_ROOT}/srunner/data/routes_town10.xml
# Town 12 Devtest Route
#export ROUTES=${LEADERBOARD_ROOT}/data/routes_devtest.xml

export ROUTES_SUBSET='' 

echo "Arguments: ${*}"

python3 ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py \
--routes=${ROUTES} \
--routes-subset=${ROUTES_SUBSET} \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--debug-checkpoint=${DEBUG_CHECKPOINT_ENDPOINT} \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME} \
${*}


