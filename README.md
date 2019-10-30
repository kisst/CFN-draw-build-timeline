# CFN-draw-build-timeline
Help to debug long running CFN builds with a visual aid in the commandline.

## Usage:
* Generate events.json:
```
    aws cloudformation describe-stack-events --stack-name mystack > events.json
```

* Visualize it with cfn-draw-build-timeline:
```
    ./timeline_build.py events.json
```
     
