export LEADERBOARD_ROOT=~/TeamProject/leaderboard

# Parameterization settings. These will be explained in 2.2. Now simply copy them to run the test.
export ROUTES=${LEADERBOARD_ROOT}/data/routes_devtest.xml
export REPETITIONS=1
export DEBUG_CHALLENGE=1
export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=MAP

# Define Team files
export TEAM_AGENT_ROOT=${PWD}
export TEAM_AGENT=${TEAM_AGENT_ROOT}/agents/leaderboard_agent.py
export TEAM_CONFIG=${TEAM_AGENT_ROOT}/conf/launch_config.yaml

export SCENARIO_RUNNER_ROOT=${TEAM_AGENT_ROOT}/scenario_runner
export PYTHONPATH=${TEAM_AGENT_ROOT}:${LEADERBOARD_ROOT}:${SCENARIO_RUNNER_ROOT}:${PYTHONPATH}

${LEADERBOARD_ROOT}/scripts/run_evaluation.sh 

