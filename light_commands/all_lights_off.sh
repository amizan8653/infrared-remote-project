#!/bin/bash

MAIN=$(cat ~/Desktop/git_repos/infrared-remote-project/light_commands/main_light_ip.txt)
CANDLE_1=$(cat ~/Desktop/git_repos/infrared-remote-project/light_commands/candle_1_light_ip.txt)
CANDLE_2=$(cat ~/Desktop/git_repos/infrared-remote-project/light_commands/candle_2_light_ip.txt)
CANDLE_3=$(cat ~/Desktop/git_repos/infrared-remote-project/light_commands/candle_3_light_ip.txt)

echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 $MAIN 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 $CANDLE_1 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 $CANDLE_2 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 $CANDLE_3 38899
