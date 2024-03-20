# Some parts of the leaderboard agent should not be merged into the main branch, e.g. the config file
# These command merge in the other files

git checkout --patch leaderboard-agent run_leaderboard_agent.sh
git checkout --patch leaderboard-agent agents/leaderboard_agent.py