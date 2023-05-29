#!/bin/bash

outputDir="output"

printf "svea\n"
convert $outputDir/svea/*.png $outputDir/svea.gif

printf "birgit\n"
convert $outputDir/birgit/*.png $outputDir/birgit.gif

printf "tom\n"
convert $outputDir/tom/*.png $outputDir/tom.gif