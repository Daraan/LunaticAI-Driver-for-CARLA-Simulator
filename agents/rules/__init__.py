# pylint: disable=unused-import
"""
Note:
    All rule should be imported into this module for insatiate to work
"""

import hydra.errors
from omegaconf import DictConfig, OmegaConf
from hydra.utils import instantiate, call
import omegaconf

from agents.rules.behaviour_templates import SetNextWaypointNearby, SlowDownAtIntersectionRule, NormalSpeedRule, ConfigBasedRSSUpdates, DEBUG_RULES
from agents.rules.lane_changes import *
from agents.rules.obstacles import *
from agents.rules.stopped_long_trigger import StoppedTooLongTrigger

from agents.tools.logging import logger

from typing import TYPE_CHECKING, Optional, Union, Iterable

from classes.constants import Phase
from classes.rule import Rule
from typing_extensions import overload

if TYPE_CHECKING:
    from classes.worldmodel import GameFramework
    from agents.tools.config_creation import RuleCreatingParameters, CreateRuleFromConfig, CallFunctionFromConfig

def create_default_rules(gameframework: Optional["GameFramework"]=None, random_lane_change: bool = False) -> "Iterable[Rule]":

    avoid_tailgator_rule = AvoidTailgatorRule()
    simple_overtake_rule = SimpleOvertakeRule()
    
    set_close_waypoint_when_done = SetNextWaypointNearby()
    normal_intersection_speed_rule = SlowDownAtIntersectionRule()
    normal_speed_rule = NormalSpeedRule()
    config_based_rss_updates = ConfigBasedRSSUpdates()
    
    #slow_towards_traffic_light = DriveSlowTowardsTrafficLight(gameframework=gameframework) # Blocking Rule

    default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, 
                           simple_overtake_rule, set_close_waypoint_when_done, config_based_rss_updates,]
    if random_lane_change:
        default_rules.append(RandomLaneChangeRule())
    
    if DEBUG_RULES:
        default_rules.append(StoppedTooLongTrigger())
        from agents.rules.behaviour_templates import SimpleRule1, SimpleRule1B, debug_rules
        default_rules.extend([SimpleRule1, SimpleRule1B])
        default_rules.extend(debug_rules)
    from classes.rule import BlockingRule
    if not gameframework and any(isinstance(rule, BlockingRule) for rule in default_rules):
        logger.warning("A BlockingRule is in the default rules but no GameFramework instance is provided. Be sure to initialize a GameFramework later!")
        
    return default_rules

@overload
def rule_from_config(cfg : "CreateRuleFromConfig") -> Rule:
    ...

@overload
def rule_from_config(cfg : "CallFunctionFromConfig | DictConfig") -> Union[Rule, Iterable[Rule]]:
    ...
    
def rule_from_config(cfg : "CallFunctionFromConfig | DictConfig | CreateRuleFromConfig") -> Union[Rule, Iterable[Rule]]:
    """
    Instantiates Rules through Hydra's instantiate function.
    
    Note:
        The _target_ interface also allows to call functions, e.g. :py:func:`create_default_rules`,
        hence you need to check if the return value is a Rule or an Iterable[Rule]
        
    Returns:
        Rule or Iterable[Rule]
        
    See Also:
        - :py:class:`agents.tools.config_creation.CreateRuleFromConfig`
        - :py:class:`agents.tools.config_creation.CallFunctionFromConfig`
    """
    if isinstance(cfg, dict):
        cfg = OmegaConf.create(cfg, flags={"allow_objects": True})
    
    # Lazy dotpath from globals
    # Allow to write NormalSpeedRule instead of agents.rules.behaviour_templates.NormalSpeedRule
    if cfg._target_ in globals():
        rule_class = globals()[cfg._target_]
        cfg._target_ = globals()[cfg._target_].__module__ + "." + cfg._target_
    else:
        rule_class = None
    # Else user needs to provide the full path
    
    # Fix phase as string from yaml
    if "phases" not in cfg or OmegaConf.is_missing(cfg, "phases") or isinstance(cfg.phases, Phase):  # type: ignore[attr-defined]
        # Target refers to a function or this will throw an error when applied to a Rule
        pass
    elif isinstance(cfg.phases, str):                      # pyright: ignore[reportAttributeAccessIssue]
        cfg.phases = Phase.from_string(cfg.phases)  # pyright: ignore[reportAttributeAccessIssue]
    elif isinstance(cfg.phases, Iterable):                 # pyright: ignore[reportAttributeAccessIssue]
        cfg.phases = [Phase.from_string(phase) if isinstance(phase, str) else phase for phase in cfg.phases]  # pyright: ignore[reportAttributeAccessIssue]
    
    # Throw out all keys that are not valid for the target, i.e. MISSING
    valid_keys = list({k for k in cfg.keys() if not OmegaConf.is_missing(cfg, k)})  # _target_ is kept for instantiate
    clean_cfg : RuleCreatingParameters = OmegaConf.masked_copy(cfg, valid_keys)  # pyright: ignore[reportArgumentType]
    
    if "_args_" in clean_cfg and clean_cfg._args_ is None:
        logger.error("_args_ argument for %s should be a list, not None", cfg._target_)
        clean_cfg._args_ = []
        
    # Note: call is an alias for instantiate
    try:
        if not "_args_" in clean_cfg:
            if "self_config" in clean_cfg:
                try:
                    # Test. If this fails, then the instantiation will also fail -> fix it
                    OmegaConf.to_container(clean_cfg, resolve=True, throw_on_missing=True)
                except (omegaconf.MissingMandatoryValue, omegaconf.errors.InterpolationKeyError) as e:
                    logger.debug("Could not resolve all values for %s, will set up a dummy parent", cfg._target_)
                    # HACK:
                    # If this fails the instantiation, OmegaConf wants to resolve the values, but as there is no parent
                    # Set a dummy config as parent
                    # TODO: should also get rid of ALL missing values
                    # Alternatively could escape all interpolations as strings and recreate the interpolations afterwards,
                    # however, need to assume that all interpolation like stings are meant as interpolations.
                    from agents.tools.config_creation import LunaticAgentSettings
                    parent : LunaticAgentSettings = OmegaConf.structured(LunaticAgentSettings(rules=[]), 
                                                                         flags={"allow_objects": True})
                    for key in parent.live_info.keys():
                        if key == "executed_direction":
                            parent.live_info[key] = "VOID"
                        try:
                            parent.live_info[key] = 0
                        except:
                            continue
                    clean_cfg.self_config._set_parent(parent)
                    clean_cfg._set_parent(parent)
                    parent["self"] = clean_cfg.self_config
                    # NOTE: If this still fails, can go over the rule_class directly if found; which might be better/easier than this hack
                
            rule: Rule = instantiate(clean_cfg, _convert_="none")
            if "self_config" in clean_cfg:
                rule.self_config.merge_with(clean_cfg.self_config) # Interpolations are resolved, adding them back as strings
            return rule
        else:
            rule_or_rules : Union[Rule, Iterable[Rule]] = call(clean_cfg, _convert_="none")
            return rule_or_rules
    except hydra.errors.InstantiationException:
        logger.error("Could not instantiate rule. The _target_ must exist in %s or you need to provide a global _target_.module.submodule... path ", __file__)
        raise


# Add rules to extracted schema
import agents.tools.config_creation as __config_creation
if not __config_creation.READTHEDOCS:
    try:
        __config_creation.export_schemas(detailed_rules=True)
    except:
        logger.exception("Error exporting schemas with rules")
del __config_creation