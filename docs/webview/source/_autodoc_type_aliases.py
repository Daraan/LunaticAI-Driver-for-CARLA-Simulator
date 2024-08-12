from typing import *


here = lambda s: "docs.webview.source._autodoc_type_aliases." + s

autodoc_type_aliases = {
    '_ActionsDictValues' : 'typing.Union[typing.Callable[[Rule, Context, ...], typing.Any], typing.Callable[[Context, ...], typing.Any]]',
    
    '_ConditionType' : "typing.Union[typing.Callable[[Rule, Context, ...], typing.Hashable], typing.Callable[[Context, ...], typing.Hashable]]",
    '_ActionType' : "typing.Union[typing.Callable[[Rule, Context, ...], typing.Any], typing.Callable[[Context, ...], typing.Any]]",
    
    'CallableAction' : "typing.Union[typing.Callable[[Rule, Context, ...], typing.Any], typing.Callable[[Context, ...], typing.Any]]",
    
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
    
    '_ActorList' : 'list',
    'Dict' : 'typing.Dict',
    'Phase' : 'classes.constants.Phase',
}

autodoc_type_aliases["_ActionTypeAlias"] = autodoc_type_aliases["_ActionType"]