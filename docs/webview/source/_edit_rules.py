def exclude_cdp():

    exclude_cdp = "\"'cleanup', 'create_blueprint', 'find_weather_presets', 'generate_spawn_points', 'get_actor_by_id', 'get_actor_by_name', 'get_local_planner', 'get_osc_global_param_value', 'get_random_seed', 'get_traffic_manager_port', 'handle_actor_batch', 'is_runtime_init_mode', 'is_sync_mode', 'on_carla_tick', 'prepare_map', 'register_actor', 'register_actors', 'remove_actor_by_id', 'remove_actors_in_surrounding', 'request_new_actor', 'request_new_actors', 'request_new_batch_actors', 'reset_lights', 'set_client', 'set_ego_route', 'set_latest_scenario', 'set_local_planner', 'set_runtime_init_mode', 'set_traffic_manager_port', 'set_world', 'spawn_actor', 'update_light_states', 'update_osc_global_params', 'world'\"".replace("'", "") #pylint: disable=line-too-long
    
    with open("classes.rst", "r+") as f:
        content = f.read()
        i = content.find(".. automodule:: classes.rule\n")
        l = len(".. automodule:: classes.rule\n")
        # Do not write double online
        if not exclude_cdp in content[i+l: i+l+len(exclude_cdp)+len("   :exclude-members: ")+1]:
            content = content[:i+l] + "   :exclude-members: " + exclude_cdp + "\n" + content[i+l:]
        else:
            return
        f.seek(0)
        f.write(content)
        