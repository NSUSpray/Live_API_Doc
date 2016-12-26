setlocal EnableDelayedExpansion
@echo off

for %%A in (..\Live*.xml) do (
	set filename=%%~nA
	set filename=!filename:Live=!
	set longversion=!filename:~3,1!
	if !longversion! neq . (set filename=!filename!.0)
	set filename=!filename!.xml
	LiveApiXmlHierarchical.py %%A !filename!
)

for %%A in (*.xml) do (
	set A_filename=%%~nA
	set A_compared=!A_filename:~5,1!
	if !A_compared! neq - (
		for %%B in (*.xml) do (
			set B_filename=%%~nB
			set B_compared=!B_filename:~5,1!
			if !B_compared! neq - (
				rem if %%B gtr %%A (echo %%A %%B)
				if %%B gtr %%A (CompareXmlTree.py %%A %%B)
			)
		)
	)
)

MakeIndex.py
