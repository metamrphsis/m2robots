#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json

def decodeFileTelemetry(fullfilepath):
    print("should be replaced by socket Json")
    try:
        with open(fullfilepath, 'r') as app2pyfile:
            app2pyData=app2pyfile.read()
            # json returns dictionary datatype, use its format as interface definition
            return json.loads(app2pyData)
    except Exception as e:
        print(e)
        telemetry = None
    return telemetry
    
    
    
    