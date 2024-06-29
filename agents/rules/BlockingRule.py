
from omegaconf import OmegaConf
import pygame
from agents.rules.behaviour_templates import DEBUG_RULES

from classes.constants import AgentState, Phase
from classes.exceptions import SkipInnerLoopException
from classes.rule import Rule, MultiRule, ConditionFunction, Context

from agents.tools.logging import logger

from typing import TYPE_CHECKING, ClassVar, List, Optional, Union

from classes.worldmodel import GameFramework

if TYPE_CHECKING:
    from agents import LunaticAgent
    from weakref import proxy
    
class BlockingRule((Rule if TYPE_CHECKING else object), metaclass=Rule):

    _gameframework: ClassVar[Union[GameFramework, "proxy[GameFramework]", None]] = None
    
    ticks_passed : int
    
    def __init__(self, *args, gameframework: Optional[GameFramework], **kwargs):
        super().__init__(*args, **kwargs)
        if gameframework:
            BlockingRule._gameframework = gameframework
        if not GameFramework.clock or not GameFramework.display:
            logger.warning("GameFramework should be initialized before using this rule.")
            GameFramework.clock, GameFramework.display = GameFramework.init_pygame()
        self.ticks_passed = 0
    
    def _render_everything(self, ctx: Context):
        if self._gameframework:
            self._gameframework.render_everything()
        else:
            world_model = ctx.agent._world_model
            display = GameFramework.display
            world_model.tick(GameFramework.clock)
            world_model.render(display, finalize=False)
            world_model.controller.render(display)
            dm_render_conf = OmegaConf.select(world_model._args, "camera.hud.data_matrix", default=None)
            
            if dm_render_conf and ctx.agent:
                ctx.agent.render_detection_matrix(display, dm_render_conf)
            world_model.finalize_render(display)
            pygame.display.flip()
    
    def loop_agent(self, ctx: Context, *, execute_phases=True):
        """
        When true, the agent will execute the Phase.UPDATE_INFORMATION | Phase.[BEGIN|END] while blocked. Default is True.
        
        Args:
            ctx (Context): The context to use
            execute_update_information (bool, optional): Whether to execute the Phase.UPDATE_INFORMATION | Phase.[BEGIN|END] while blocked. Defaults to True.
        
        TODO:
            Add a Phases.PHASE_CHANGE_BLOCKED flag.
        """

        # Tick world and render everything
        self._render_everything(ctx)
        self.ticks_passed += 1

        # Update the agent's information
        if execute_phases:
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=self)
        ctx.agent._update_information()
        if execute_phases:
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=self)
        # TODO: What about UpdatePathException?

    def __call__(self, ctx: Context, overwrite=None, *args, in_loop=False, **kwargs):
        if not in_loop:
            self.ticks_passed = 0
        else:
            kwargs.setdefault("ignore_phase", True)
            kwargs.setdefault("ignore_cooldown", True)
        return super().__call__(ctx, overwrite, *args, **kwargs)
            
    def action(self, ctx: Context):
        import carla
        result = True
        while result == True and self.ticks_passed < 50:
            if self.ticks_passed < 20:
                control = carla.VehicleControl(reverse=True, throttle=0.2)
                ctx.agent.apply_control(control)
            self.loop_agent(ctx)
            result = self.condition(ctx)
        ctx.control = carla.VehicleControl()
        raise SkipInnerLoopException(ctx.control)
        

        
        
        


