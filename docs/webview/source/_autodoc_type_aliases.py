from typing import *
import typing


here = lambda s: "docs.webview.source._autodoc_type_aliases." + s

autodoc_type_aliases = {
    '_ActionsDictValues' : 'typing.Union[typing.Callable[typing.Concatenate[Rule, Context, ...], typing.Any], typing.Callable[typing.Concatenate[Context, ...], typing.Any]]',
    
    '_ConditionType' : "typing.Union[typing.Callable[typing.Concatenate[Rule, Context, ...], typing.Hashable], typing.Callable[typing.Concatenate[Context, ...], typing.Hashable]]",
    '_ActionType' : "typing.Union[typing.Callable[typing.Concatenate[Rule, Context, ...], typing.Any], typing.Callable[typing.Concatenate[Context, ...], typing.Any]]",
    
    'CallableAction' : "typing.Union[typing.Callable[typing.Concatenate[Rule, Context, ...], typing.Any], typing.Callable[typing.Concatenate[Context, ...], typing.Any]]",
    '_CallableCondition' : "typing.Union[typing.Callable[typing.Concatenate[Rule, Context, ...], typing.Hashable], typing.Callable[typing.Concatenate[Context, ...], typing.Hashable]]",
    
    'CallableAction' : "classes.type_protocols.CallableActionT",
    'CallableCondition' : "classes.type_protocols.CallableConditionT",
    
    '_RegisterActionDecorator' : "Callable[[classes.type_protocols.CallableAction], classes.type_protocols.CallableAction]",
    
    'CallableCondition[RuleT, _CP, _CH]' : "CallableConditionT",
    
    'CallableAction[Self, [], Any],' : "CallableActionT",
    
    '_Rule' : "Rule",
    '_CP' : 'typing.ParamSpec',
    '_P' : 'typing.ParamSpec',
    'kwargs' : 'ParamSpecKwargs',
    '_P.kwargs' : 'ParamSpecKwargs',
    
    '_H' : 'typing.Hashable',
    #'_CH' : 'typing.Hashable', # only use one _H
    '_T' : 'typing.Any',
    'Optional' : 'typing.Optional',
    'partial' : 'functools.partial',
    
    'Annotated' : 'typing.Annotated',
    'ClassVar' : 'typing.ClassVar',
    'Context' : 'classes.rule.Context',
    
    '_ActionsDictValues' : 'AnyCallableAction',
    
    '_ActorList' : 'list',
    
    #'ConditionFunctionLikeT' : "ConditionFunction | Callable[typing.Concatenate[Rule, Context, ...], typing.Any] | typing.Callable[typing.Concatenate[Context, ...], typing.Any]"
    #'Dict' : 'typing.Dict',
    #'Phase' : 'classes.constants.Phase',
    #'NoReturn' : 'typing.NoReturn',
    #'FrozenSet' : 'typing.FrozenSet',
    #'Iterable' : 'typing.Iterable',
}

#from inspect import ismodule

#autodoc_type_aliases.update(map(lambda x: (x[0], "typing." + x[0]),
#    filter(lambda x: not x[0].startswith("_") and len(x[0]) > 3 and not ismodule(x[1]), typing.__dict__.items())))

#autodoc_type_aliases["_ActionTypeAlias"] = autodoc_type_aliases["_ActionType"]

