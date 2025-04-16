#!/bin/bash

echo -n "{\"id\":1,\"method\":\"setPilot\",\"params\":{\"sceneId\":12,\"dimming\":100}}" | nc -u -w 1 192.168.4.21 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 192.168.4.78 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 192.168.4.79 38899 \
& echo -n "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}" | nc -u -w 1 192.168.4.80 38899
